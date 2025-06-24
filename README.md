# Amazon Nova Reel 1.1 MCP Server

A Model Context Protocol (MCP) server for Amazon Nova Reel 1.1 video generation using AWS Bedrock. This server provides tools for asynchronous video generation with comprehensive prompting guidelines and both stdio and SSE transport support.

<div align="center">
  
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/mirecekdg)

</div>


## Features

- **Asynchronous Video Generation**: Start, monitor, and retrieve video generation jobs
- **Multiple Transport Methods**: Support for both stdio and Server-Sent Events (SSE)
- **Comprehensive Prompting Guide**: Built-in guidelines based on AWS documentation
- **Docker Support**: Ready-to-use Docker containers for both transport methods
- **AWS Integration**: Full integration with AWS Bedrock and S3

## Available Tools

### 1. `start_async_invoke`
Start a new video generation job.

**Parameters:**
- `prompt` (required): Text description for video generation
- `duration_seconds` (optional): Video duration (12-120 seconds, multiples of 6, default: 12)
- `fps` (optional): Frames per second (default: 24)
- `dimension` (optional): Video dimensions (default: "1280x720")
- `seed` (optional): Random seed for reproducible results
- `task_type` (optional): Task type (default: "MULTI_SHOT_AUTOMATED")

**Returns:** Job details including `job_id`, `invocation_arn`, and estimated video URL.

### 2. `list_async_invokes`
List all tracked video generation jobs with their current status.

**Returns:** Summary of all jobs with status counts and individual job details.

### 3. `get_async_invoke`
Get detailed information about a specific video generation job.

**Parameters:**
- `identifier` (required): Either `job_id` or `invocation_arn`

**Returns:** Detailed job information including video URL when completed.

### 4. `get_prompting_guide`
Get comprehensive prompting guidelines for effective video generation.

**Returns:** Detailed prompting best practices, examples, and templates.

## Installation

### Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- S3 bucket for video output
- AWS credentials with appropriate permissions

### Local Installation

1. Clone or download the server files
2. Install dependencies:
```bash
pip install -e .
```

### Docker Installation

#### Using Pre-built Images (Recommended)

Pull multi-architecture images from GitHub Container Registry:

```bash
# STDIO version
docker pull ghcr.io/mirecekd/novareel-mcp:latest-stdio

# SSE version  
docker pull ghcr.io/mirecekd/novareel-mcp:latest-sse
```

#### Building Locally

1. Build containers using provided scripts:
```bash
# Build all versions
./build-all.sh

# Or build individual versions
./build-stdio.sh    # STDIO version
./build-sse.sh      # SSE version
```

2. Or use docker-compose:
```bash
docker-compose up -d
```

3. Or use the quick start script:
```bash
# Build all images
./start.sh build

# Build specific version
./start.sh build-stdio
./start.sh build-sse
```

## Configuration

### Environment Variables

- `AWS_ACCESS_KEY_ID`: Your AWS access key ID
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key
- `AWS_REGION`: AWS region (default: us-east-1)
- `S3_BUCKET`: S3 bucket name for video output

### .env File Example

Create a `.env` file for docker-compose:

```env
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=us-east-1
S3_BUCKET=my-video-generation-bucket
```

## Usage

### MCP Client Integration (Cline/Claude Desktop)

Add the server to your MCP client configuration:

#### Cline Configuration
Add to your Cline MCP settings:

```json
{
  "mcpServers": {
    "Nova Reel Video MCP": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "--env", "AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID",
        "--env", "AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY", 
        "--env", "AWS_REGION=us-east-1",
        "--env", "S3_BUCKET=YOUR_S3_BUCKET_NAME",
        "ghcr.io/mirecekd/novareel-mcp:latest-stdio"
      ]
    }
  }
}
```

#### Claude Desktop Configuration
Add to your Claude Desktop `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "novareel-mcp": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "--env", "AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID",
        "--env", "AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY",
        "--env", "AWS_REGION=us-east-1", 
        "--env", "S3_BUCKET=YOUR_S3_BUCKET_NAME",
        "ghcr.io/mirecekd/novareel-mcp:latest-stdio"
      ]
    }
  }
}
```

#### Alternative: Local Python Installation
If you prefer running without Docker:

```json
{
  "mcpServers": {
    "novareel-mcp": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/mirecekd/novareel-mcp.git",
        "novareel-mcp-server",
        "--aws-access-key-id", "YOUR_AWS_ACCESS_KEY_ID",
        "--aws-secret-access-key", "YOUR_AWS_SECRET_ACCESS_KEY",
        "--s3-bucket", "YOUR_S3_BUCKET_NAME"
      ]
    }
  }
}
```

**Important**: Replace the placeholder values with your actual AWS credentials and S3 bucket name.

### Running with uvx (Recommended)

```bash
# First build the package
./build.sh

# Then run from wheel file
uvx --from ./dist/novareel_mcp-1.0.0-py3-none-any.whl novareel-mcp-server --aws-access-key-id YOUR_KEY --aws-secret-access-key YOUR_SECRET --s3-bucket YOUR_BUCKET

# Or from current directory during development (without build)
uvx --from . novareel-mcp-server --aws-access-key-id YOUR_KEY --aws-secret-access-key YOUR_SECRET --s3-bucket YOUR_BUCKET

# Or using start script
./start.sh build-package  # Build wheel
```

### Stdio Version (Direct MCP Client)

```bash
# Local execution
python main.py --aws-access-key-id YOUR_KEY --aws-secret-access-key YOUR_SECRET --s3-bucket YOUR_BUCKET

# Docker execution
docker run --rm -i mirecekd/novareel-mcp-server:stdio --aws-access-key-id YOUR_KEY --aws-secret-access-key YOUR_SECRET --s3-bucket YOUR_BUCKET
```

### SSE Version (Web Interface)

```bash
# Local execution
python -m novareel_mcp_server.server_sse --aws-access-key-id YOUR_KEY --aws-secret-access-key YOUR_SECRET --s3-bucket YOUR_BUCKET --host 0.0.0.0 --port 8000

# Docker execution
docker run -p 8000:8000 -e AWS_ACCESS_KEY_ID=YOUR_KEY -e AWS_SECRET_ACCESS_KEY=YOUR_SECRET -e S3_BUCKET=YOUR_BUCKET mirecekd/novareel-mcp-server:sse
```

Then access `http://localhost:8000` for the web interface.

### Package Build

To create a distribution package:

```bash
# Install build tools
pip install build

# Create package
python3 -m build

# Output files will be in dist/
```

## Example Usage

### Basic Video Generation

```python
# Start a video generation job
result = start_async_invoke(
    prompt="A majestic eagle soars over a mountain valley, camera tracking its flight as it circles above a pristine lake",
    duration_seconds=24,
    fps=24,
    dimension="1920x1080"
)

job_id = result["job_id"]
print(f"Started job: {job_id}")

# Check job status
status = get_async_invoke(job_id)
print(f"Status: {status['status']}")

# When completed, get video URL
if status["status"] == "Completed":
    print(f"Video URL: {status['video_url']}")
```

### List All Jobs

```python
# Get overview of all jobs
jobs = list_async_invokes()
print(f"Total jobs: {jobs['total_invocations']}")
print(f"Completed: {jobs['summary']['completed']}")
print(f"In progress: {jobs['summary']['in_progress']}")
```

## Prompting Guidelines

The server includes comprehensive prompting guidelines based on AWS documentation. Access them using:

```python
guide = get_prompting_guide()
```

### Key Prompting Tips

1. **Be Specific**: Use detailed, descriptive language
   - Good: "A red cardinal perched on a snow-covered pine branch, morning sunlight filtering through the trees"
   - Bad: "A bird on a tree"

2. **Use Camera Terminology**: Control shot composition
   - "Close-up shot of hands carving wood"
   - "Wide shot establishing the mountain landscape"
   - "Camera pans left across the valley"

3. **Include Lighting Details**: Specify atmosphere
   - "Golden hour lighting casting long shadows"
   - "Soft blue hour twilight"
   - "Dramatic storm clouds overhead"

4. **Structure for Duration**: Match complexity to video length
   - 12-24 seconds: Single action or moment
   - 30-60 seconds: 2-3 distinct actions
   - 60-120 seconds: Full narrative with multiple scenes

### Example Prompts by Category

**Nature (Short - 12s):**
```
Close-up of morning dew drops on a spider web, with soft sunrise lighting creating rainbow reflections
```

**Urban (Medium - 30s):**
```
A street musician plays violin in a subway station, commuters pause to listen, coins drop into his case, camera slowly pulls back to reveal the bustling underground scene
```

**Portrait (Long - 60s):**
```
Portrait of a chef preparing a signature dish: selecting fresh ingredients at market, returning to kitchen, methodically preparing each component, plating with artistic precision, and presenting the finished masterpiece
```

## AWS Permissions

Your AWS credentials need the following permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:StartAsyncInvoke",
                "bedrock:GetAsyncInvoke",
                "bedrock:ListFoundationModels"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name",
                "arn:aws:s3:::your-bucket-name/*"
            ]
        }
    ]
}
```

## Video Output

Generated videos are stored in your S3 bucket with the following structure:
```
s3://your-bucket/
├── job-id-1/
│   └── output.mp4
├── job-id-2/
│   └── output.mp4
└── ...
```

Videos are accessible via HTTPS URLs:
```
https://your-bucket.s3.region.amazonaws.com/job-id/output.mp4
```

## Supported Video Specifications

- **Duration**: 12-120 seconds (must be multiples of 6)
- **Frame Rate**: 24 fps (recommended)
- **Dimensions**: 
  - 1280x720 (HD)
- **Format**: MP4
- **Model**: amazon.nova-reel-v1:1

## Troubleshooting

### Common Issues

1. **AWS Credentials Error**
   - Verify your AWS credentials are correct
   - Ensure your account has Bedrock access enabled
   - Check IAM permissions

2. **S3 Bucket Access**
   - Verify bucket exists and is accessible
   - Check bucket permissions
   - Ensure bucket is in the same region as Bedrock

3. **Duration Validation**
   - Duration must be 12-120 seconds
   - Must be a multiple of 6
   - Valid values: 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96, 102, 108, 114, 120

4. **Job Not Found**
   - Use `list_async_invokes` to see all tracked jobs
   - Jobs are stored in memory and lost on server restart
   - For production, implement persistent storage

### Debug Mode

Enable debug logging by setting environment variable:
```bash
export PYTHONUNBUFFERED=1
```

## Development

### Project Structure

```
novareel-mcp-server/
├── main.py              # Main MCP server (stdio)
├── main_sse.py          # SSE version of MCP server
├── prompting_guide.py   # AWS prompting guidelines
├── pyproject.toml       # Python dependencies
├── Dockerfile.stdio     # Docker for stdio version
├── Dockerfile.sse       # Docker for SSE version
├── docker-compose.yml   # Container orchestration
└── README.md           # This documentation
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with both stdio and SSE versions
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review AWS Bedrock documentation
3. Open an issue in the repository

## Related Links

- [AWS Nova Reel Documentation](https://docs.aws.amazon.com/nova/latest/userguide/)
- [Video Generation Prompting Guide](https://docs.aws.amazon.com/nova/latest/userguide/prompting-video-generation.html)
- [Camera Control Prompting](https://docs.aws.amazon.com/nova/latest/userguide/prompting-video-camera-control.html)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
