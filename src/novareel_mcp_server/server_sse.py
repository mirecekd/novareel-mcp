#!/usr/bin/env python3
"""
Amazon Nova Reel 1.1 MCP Server - SSE Version
Provides tools for video generation using AWS Bedrock Nova Reel model via Server-Sent Events.
"""

import argparse
import asyncio
import json
import os
import sys
import random
import time
from datetime import datetime
from typing import Optional, Dict, Any, List
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from fastmcp import FastMCP
from .prompting_guide import get_prompting_guidelines

# Create MCP server with SSE transport
mcp = FastMCP("Amazon Nova Reel 1.1 SSE")

# Global variables for AWS configuration
aws_access_key_id: Optional[str] = None
aws_secret_access_key: Optional[str] = None
aws_session_token: Optional[str] = None
aws_profile: Optional[str] = None
aws_region: Optional[str] = None
s3_bucket: Optional[str] = None
bedrock_client = None

# Model configuration
MODEL_ID = "amazon.nova-reel-v1:1"
SLEEP_SECONDS = 5  # Interval for checking video generation progress

# In-memory storage for tracking invocations (in production, use persistent storage)
active_invocations = {}


class NovaReelError(Exception):
    """Base exception for Nova Reel operations"""
    pass


class AWSConfigError(NovaReelError):
    """AWS configuration error"""
    pass


class VideoGenerationError(NovaReelError):
    """Video generation error"""
    pass


def initialize_aws_client():
    """Initialize AWS Bedrock client with provided credentials or profile"""
    global bedrock_client
    
    if not s3_bucket:
        raise AWSConfigError("Missing required S3_BUCKET configuration")
    
    try:
        # Option 1: Use AWS Profile
        if aws_profile:
            print(f"Using AWS profile: {aws_profile}", file=sys.stderr)
            session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
            bedrock_client = session.client("bedrock-runtime")
            
        # Option 2: Use explicit credentials
        elif aws_access_key_id and aws_secret_access_key:
            print("Using explicit AWS credentials", file=sys.stderr)
            client_kwargs = {
                "service_name": "bedrock-runtime",
                "region_name": aws_region,
                "aws_access_key_id": aws_access_key_id,
                "aws_secret_access_key": aws_secret_access_key
            }
            
            # Add session token if provided (for temporary credentials)
            if aws_session_token:
                client_kwargs["aws_session_token"] = aws_session_token
                print("Using temporary credentials with session token", file=sys.stderr)
            
            bedrock_client = boto3.client(**client_kwargs)
            
        # Option 3: Use default credential chain
        else:
            print("Using default AWS credential chain", file=sys.stderr)
            bedrock_client = boto3.client("bedrock-runtime", region_name=aws_region)
        
        # Test the connection with a simple operation
        # Note: bedrock-runtime doesn't have list_foundation_models, that's in bedrock client
        # We'll just create the client and let the first actual call test the connection
        
    except NoCredentialsError:
        raise AWSConfigError("No valid AWS credentials found. Please provide explicit credentials, set AWS_PROFILE, or configure default credentials.")
    except ClientError as e:
        raise AWSConfigError(f"AWS client error: {e}")
    except Exception as e:
        raise AWSConfigError(f"Failed to initialize AWS client: {e}")


@mcp.tool()
async def start_async_invoke(
    prompt: str,
    duration_seconds: int = 12,
    fps: int = 24,
    dimension: str = "1280x720",
    seed: Optional[int] = None,
    task_type: str = "MULTI_SHOT_AUTOMATED"
) -> Dict[str, Any]:
    """
    Start asynchronous video generation with Amazon Nova Reel.
    
    Args:
        prompt: Text description for video generation. See prompting guidelines for best practices.
        duration_seconds: Video duration in seconds (must be multiple of 6, range 12-120)
        fps: Frames per second (24 recommended)
        dimension: Video dimensions (1280x720, 1920x1080, etc.)
        seed: Random seed for reproducible results (optional)
        task_type: Task type (MULTI_SHOT_AUTOMATED recommended)
    
    Returns:
        Dict containing invocation details and job information
    """
    try:
        if not bedrock_client:
            initialize_aws_client()
        
        # Validate duration
        if duration_seconds < 12 or duration_seconds > 120 or duration_seconds % 6 != 0:
            return {
                "error": "Duration must be a multiple of 6 in range [12, 120]",
                "valid_durations": [12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96, 102, 108, 114, 120]
            }
        
        # Generate seed if not provided
        if seed is None:
            seed = random.randint(0, 2147483648)
        
        # Prepare model input
        model_input = {
            "taskType": task_type,
            "multiShotAutomatedParams": {"text": prompt},
            "videoGenerationConfig": {
                "durationSeconds": duration_seconds,
                "fps": fps,
                "dimension": dimension,
                "seed": seed,
            },
        }
        
        # Start async invocation
        invocation = bedrock_client.start_async_invoke(
            modelId=MODEL_ID,
            modelInput=model_input,
            outputDataConfig={"s3OutputDataConfig": {"s3Uri": f"s3://{s3_bucket}"}},
        )
        
        invocation_arn = invocation["invocationArn"]
        job_id = invocation_arn.split("/")[-1]
        s3_location = f"s3://{s3_bucket}/{job_id}"
        
        # Store invocation details
        invocation_data = {
            "invocation_arn": invocation_arn,
            "job_id": job_id,
            "prompt": prompt,
            "duration_seconds": duration_seconds,
            "fps": fps,
            "dimension": dimension,
            "seed": seed,
            "task_type": task_type,
            "s3_location": s3_location,
            "status": "InProgress",
            "created_at": datetime.now().isoformat(),
            "video_url": None
        }
        
        active_invocations[job_id] = invocation_data
        
        return {
            "success": True,
            "invocation_arn": invocation_arn,
            "job_id": job_id,
            "status": "InProgress",
            "s3_location": s3_location,
            "estimated_video_url": f"https://{s3_bucket}.s3.{aws_region}.amazonaws.com/{job_id}/output.mp4",
            "prompt": prompt,
            "config": {
                "duration_seconds": duration_seconds,
                "fps": fps,
                "dimension": dimension,
                "seed": seed
            },
            "message": "Video generation started. Use get_async_invoke to check progress."
        }
        
    except AWSConfigError as e:
        return {"error": f"AWS configuration error: {e}"}
    except ClientError as e:
        return {"error": f"AWS API error: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}


@mcp.tool()
async def list_async_invokes() -> Dict[str, Any]:
    """
    List all tracked async video generation invocations.
    
    Returns:
        Dict containing list of all invocations with their current status
    """
    try:
        if not bedrock_client:
            initialize_aws_client()
        
        # Update status for all active invocations
        updated_invocations = []
        
        for job_id, invocation_data in active_invocations.items():
            try:
                # Get current status from AWS
                response = bedrock_client.get_async_invoke(
                    invocationArn=invocation_data["invocation_arn"]
                )
                
                # Update status
                current_status = response["status"]
                invocation_data["status"] = current_status
                
                if current_status == "Completed":
                    invocation_data["video_url"] = f"https://{s3_bucket}.s3.{aws_region}.amazonaws.com/{job_id}/output.mp4"
                    invocation_data["completed_at"] = datetime.now().isoformat()
                elif current_status in ["Failed", "Cancelled"]:
                    invocation_data["failed_at"] = datetime.now().isoformat()
                    if "failureMessage" in response:
                        invocation_data["failure_message"] = response["failureMessage"]
                
                updated_invocations.append({
                    "job_id": job_id,
                    "status": current_status,
                    "prompt": invocation_data["prompt"][:100] + "..." if len(invocation_data["prompt"]) > 100 else invocation_data["prompt"],
                    "created_at": invocation_data["created_at"],
                    "video_url": invocation_data.get("video_url"),
                    "duration_seconds": invocation_data["duration_seconds"]
                })
                
            except ClientError as e:
                # If we can't get status, mark as unknown
                invocation_data["status"] = "Unknown"
                invocation_data["error"] = str(e)
                updated_invocations.append({
                    "job_id": job_id,
                    "status": "Unknown",
                    "prompt": invocation_data["prompt"][:100] + "..." if len(invocation_data["prompt"]) > 100 else invocation_data["prompt"],
                    "created_at": invocation_data["created_at"],
                    "error": str(e)
                })
        
        return {
            "success": True,
            "total_invocations": len(updated_invocations),
            "invocations": updated_invocations,
            "summary": {
                "in_progress": len([inv for inv in updated_invocations if inv["status"] == "InProgress"]),
                "completed": len([inv for inv in updated_invocations if inv["status"] == "Completed"]),
                "failed": len([inv for inv in updated_invocations if inv["status"] in ["Failed", "Cancelled"]]),
                "unknown": len([inv for inv in updated_invocations if inv["status"] == "Unknown"])
            }
        }
        
    except AWSConfigError as e:
        return {"error": f"AWS configuration error: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}


@mcp.tool()
async def get_async_invoke(identifier: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific async video generation invocation.
    
    Args:
        identifier: Either job_id or invocation_arn
    
    Returns:
        Dict containing detailed invocation information and video URL if completed
    """
    try:
        if not bedrock_client:
            initialize_aws_client()
        
        # Find invocation by job_id or invocation_arn
        invocation_data = None
        job_id = None
        
        if identifier in active_invocations:
            # Direct job_id lookup
            job_id = identifier
            invocation_data = active_invocations[identifier]
        else:
            # Search by invocation_arn
            for jid, data in active_invocations.items():
                if data["invocation_arn"] == identifier:
                    job_id = jid
                    invocation_data = data
                    break
        
        if not invocation_data:
            return {
                "error": f"Invocation not found: {identifier}",
                "suggestion": "Use list_async_invokes to see all tracked invocations"
            }
        
        # Get current status from AWS
        try:
            response = bedrock_client.get_async_invoke(
                invocationArn=invocation_data["invocation_arn"]
            )
            
            current_status = response["status"]
            invocation_data["status"] = current_status
            
            # Prepare detailed response
            result = {
                "success": True,
                "job_id": job_id,
                "invocation_arn": invocation_data["invocation_arn"],
                "status": current_status,
                "prompt": invocation_data["prompt"],
                "config": {
                    "duration_seconds": invocation_data["duration_seconds"],
                    "fps": invocation_data["fps"],
                    "dimension": invocation_data["dimension"],
                    "seed": invocation_data["seed"],
                    "task_type": invocation_data["task_type"]
                },
                "s3_location": invocation_data["s3_location"],
                "created_at": invocation_data["created_at"]
            }
            
            if current_status == "Completed":
                video_url = f"https://{s3_bucket}.s3.{aws_region}.amazonaws.com/{job_id}/output.mp4"
                invocation_data["video_url"] = video_url
                invocation_data["completed_at"] = datetime.now().isoformat()
                
                result["video_url"] = video_url
                result["completed_at"] = invocation_data["completed_at"]
                result["message"] = "Video generation completed successfully!"
                
            elif current_status == "InProgress":
                result["message"] = "Video generation is still in progress. Check again in a few moments."
                
            elif current_status in ["Failed", "Cancelled"]:
                invocation_data["failed_at"] = datetime.now().isoformat()
                result["failed_at"] = invocation_data["failed_at"]
                result["message"] = f"Video generation {current_status.lower()}"
                
                if "failureMessage" in response:
                    result["failure_message"] = response["failureMessage"]
                    invocation_data["failure_message"] = response["failureMessage"]
            
            return result
            
        except ClientError as e:
            return {
                "error": f"Failed to get invocation status: {e}",
                "job_id": job_id,
                "last_known_status": invocation_data.get("status", "Unknown")
            }
        
    except AWSConfigError as e:
        return {"error": f"AWS configuration error: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}


@mcp.tool()
async def get_prompting_guide() -> Dict[str, Any]:
    """
    Get comprehensive prompting guidelines for Amazon Nova Reel video generation.
    
    Returns:
        Dict containing prompting best practices and examples
    """
    return get_prompting_guidelines()


def main():
    """Main function to run the MCP server with SSE transport"""
    parser = argparse.ArgumentParser(description="Amazon Nova Reel 1.1 MCP Server - SSE Version")
    parser.add_argument("--aws-access-key-id", help="AWS Access Key ID")
    parser.add_argument("--aws-secret-access-key", help="AWS Secret Access Key")
    parser.add_argument("--aws-session-token", help="AWS Session Token (for temporary credentials)")
    parser.add_argument("--aws-profile", help="AWS Profile name (alternative to explicit credentials)")
    parser.add_argument("--aws-region", default="us-east-1", help="AWS Region")
    parser.add_argument("--s3-bucket", help="S3 bucket name for video output")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    
    args = parser.parse_args()
    
    # Set global configuration from args or environment variables
    global aws_access_key_id, aws_secret_access_key, aws_session_token, aws_profile, aws_region, s3_bucket
    
    aws_access_key_id = args.aws_access_key_id or os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = args.aws_secret_access_key or os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_session_token = args.aws_session_token or os.getenv("AWS_SESSION_TOKEN")
    aws_profile = args.aws_profile or os.getenv("AWS_PROFILE")
    aws_region = args.aws_region or os.getenv("AWS_REGION", "us-east-1")
    s3_bucket = args.s3_bucket or os.getenv("S3_BUCKET")
    
    # Validate configuration - need either profile OR explicit credentials + S3 bucket
    if not s3_bucket:
        print("Error: Missing required S3_BUCKET configuration.", file=sys.stderr)
        print("Please provide --s3-bucket or S3_BUCKET env var", file=sys.stderr)
        sys.exit(1)
    
    # Check if we have valid credential configuration
    has_explicit_creds = aws_access_key_id and aws_secret_access_key
    has_profile = aws_profile
    
    if not has_explicit_creds and not has_profile:
        print("Error: Missing AWS credentials configuration.", file=sys.stderr)
        print("Please provide either:", file=sys.stderr)
        print("  Option 1: --aws-access-key-id and --aws-secret-access-key (with optional --aws-session-token)", file=sys.stderr)
        print("  Option 2: --aws-profile", file=sys.stderr)
        print("  Option 3: Set corresponding environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_PROFILE)", file=sys.stderr)
        print("  Option 4: Configure default AWS credentials (e.g., via aws configure)", file=sys.stderr)
        sys.exit(1)
    
    if has_explicit_creds and has_profile:
        print("Warning: Both explicit credentials and AWS profile provided. Using explicit credentials.", file=sys.stderr)
        aws_profile = None  # Clear profile to avoid confusion
    
    # Remove s3:// prefix if present
    if s3_bucket.startswith("s3://"):
        s3_bucket = s3_bucket[5:]
    
    # Initialize AWS client
    try:
        initialize_aws_client()
        print(f"Nova Reel MCP Server (SSE) initialized with region: {aws_region}, bucket: {s3_bucket}", file=sys.stderr)
        print(f"Starting server on {args.host}:{args.port}", file=sys.stderr)
    except AWSConfigError as e:
        print(f"AWS configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Run MCP server with SSE transport
    mcp.run(transport="sse", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
