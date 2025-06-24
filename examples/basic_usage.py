#!/usr/bin/env python3
"""
Basic usage example for Nova Reel MCP Server
This example demonstrates how to generate a simple video using the MCP server.
"""

import asyncio
import json
import sys
import os

# Add parent directory to path to import the server modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import start_async_invoke, get_async_invoke, list_async_invokes, get_prompting_guide

async def basic_video_generation():
    """
    Example of basic video generation workflow
    """
    print("🎬 Nova Reel MCP Server - Basic Usage Example")
    print("=" * 50)
    
    # Example prompt for a nature scene
    prompt = """
    A majestic eagle soars over a mountain valley at golden hour, 
    camera tracking its flight as it circles above a pristine lake, 
    then dives gracefully toward the water surface
    """
    
    print(f"📝 Prompt: {prompt.strip()}")
    print()
    
    try:
        # Start video generation
        print("🚀 Starting video generation...")
        result = await start_async_invoke(
            prompt=prompt,
            duration_seconds=24,  # 24 second video
            fps=24,
            dimension="1920x1080"  # Full HD
        )
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return
        
        job_id = result["job_id"]
        print(f"✅ Job started successfully!")
        print(f"   Job ID: {job_id}")
        print(f"   Status: {result['status']}")
        print(f"   Estimated URL: {result['estimated_video_url']}")
        print()
        
        # Monitor progress
        print("⏳ Monitoring progress...")
        max_attempts = 60  # Wait up to 5 minutes (60 * 5 seconds)
        attempt = 0
        
        while attempt < max_attempts:
            status_result = await get_async_invoke(job_id)
            
            if "error" in status_result:
                print(f"❌ Error checking status: {status_result['error']}")
                break
            
            current_status = status_result["status"]
            print(f"   Status: {current_status} (attempt {attempt + 1}/{max_attempts})")
            
            if current_status == "Completed":
                print("🎉 Video generation completed!")
                print(f"   Video URL: {status_result['video_url']}")
                print(f"   Duration: {status_result['config']['duration_seconds']} seconds")
                print(f"   Dimensions: {status_result['config']['dimension']}")
                break
            elif current_status in ["Failed", "Cancelled"]:
                print(f"❌ Video generation {current_status.lower()}")
                if "failure_message" in status_result:
                    print(f"   Reason: {status_result['failure_message']}")
                break
            
            # Wait 5 seconds before checking again
            await asyncio.sleep(5)
            attempt += 1
        
        if attempt >= max_attempts:
            print("⏰ Timeout reached. Video may still be processing.")
            print("   Use get_async_invoke() to check status later.")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

async def list_all_jobs():
    """
    Example of listing all video generation jobs
    """
    print("\n📋 Listing all jobs...")
    print("-" * 30)
    
    try:
        jobs_result = await list_async_invokes()
        
        if "error" in jobs_result:
            print(f"❌ Error: {jobs_result['error']}")
            return
        
        total = jobs_result["total_invocations"]
        summary = jobs_result["summary"]
        
        print(f"Total jobs: {total}")
        print(f"  ✅ Completed: {summary['completed']}")
        print(f"  ⏳ In Progress: {summary['in_progress']}")
        print(f"  ❌ Failed: {summary['failed']}")
        print(f"  ❓ Unknown: {summary['unknown']}")
        print()
        
        if total > 0:
            print("Recent jobs:")
            for job in jobs_result["invocations"][:5]:  # Show last 5 jobs
                status_emoji = {
                    "Completed": "✅",
                    "InProgress": "⏳",
                    "Failed": "❌",
                    "Cancelled": "❌",
                    "Unknown": "❓"
                }.get(job["status"], "❓")
                
                print(f"  {status_emoji} {job['job_id'][:8]}... - {job['status']}")
                print(f"     Prompt: {job['prompt'][:60]}...")
                if job.get("video_url"):
                    print(f"     URL: {job['video_url']}")
                print()
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

async def show_prompting_tips():
    """
    Example of getting prompting guidelines
    """
    print("\n💡 Prompting Guidelines")
    print("=" * 30)
    
    try:
        guide = await get_prompting_guide()
        
        # Show basic principles
        print("Basic Principles:")
        for principle, details in guide["basic_principles"].items():
            print(f"\n🔹 {principle.replace('_', ' ').title()}:")
            print(f"   {details['description']}")
            print(f"   ✅ Good: {details['good_example']}")
            print(f"   ❌ Bad: {details['bad_example']}")
        
        # Show example prompts
        print("\n\n📝 Example Prompts:")
        examples = guide["example_prompts"]
        
        for category, prompts in examples.items():
            print(f"\n🎯 {category.title()}:")
            for duration, prompt in prompts.items():
                print(f"   {duration.replace('_', ' ').title()}: {prompt}")
        
        # Show common mistakes
        print("\n\n⚠️  Common Mistakes to Avoid:")
        for mistake, details in guide["common_mistakes"].items():
            print(f"\n❌ {details['problem']}")
            print(f"   Example: {details['example']}")
            print(f"   Solution: {details['solution']}")
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

async def main():
    """
    Main example function
    """
    print("Welcome to Nova Reel MCP Server Examples!")
    print("This example will demonstrate basic video generation.")
    print()
    
    # Check if AWS credentials are configured
    if not all([
        os.getenv("AWS_ACCESS_KEY_ID"),
        os.getenv("AWS_SECRET_ACCESS_KEY"),
        os.getenv("S3_BUCKET")
    ]):
        print("⚠️  AWS credentials not configured!")
        print("Please set the following environment variables:")
        print("  - AWS_ACCESS_KEY_ID")
        print("  - AWS_SECRET_ACCESS_KEY")
        print("  - S3_BUCKET")
        print("  - AWS_REGION (optional, defaults to us-east-1)")
        print()
        print("Example:")
        print("  export AWS_ACCESS_KEY_ID=your_access_key")
        print("  export AWS_SECRET_ACCESS_KEY=your_secret_key")
        print("  export S3_BUCKET=your-bucket-name")
        print("  python examples/basic_usage.py")
        return
    
    # Show prompting tips first
    await show_prompting_tips()
    
    # Generate a video
    await basic_video_generation()
    
    # List all jobs
    await list_all_jobs()
    
    print("\n🎉 Example completed!")
    print("Check your S3 bucket for the generated video.")

if __name__ == "__main__":
    # Note: This example assumes the MCP server functions are available
    # In a real scenario, you would interact with the MCP server via the protocol
    print("📝 Note: This is a conceptual example.")
    print("In practice, you would interact with the MCP server through an MCP client.")
    print("This example shows the expected workflow and API usage.")
    
    # Run the example
    asyncio.run(main())
