"""
Amazon Nova Reel Prompting Guidelines
Based on AWS documentation for video generation and camera control.
"""

def get_prompting_guidelines():
    """
    Returns comprehensive prompting guidelines for Amazon Nova Reel video generation.
    Based on AWS documentation:
    - https://docs.aws.amazon.com/nova/latest/userguide/prompting-video-generation.html
    - https://docs.aws.amazon.com/nova/latest/userguide/prompting-video-camera-control.html
    """
    
    return {
        "overview": {
            "title": "Amazon Nova Reel Video Generation Prompting Guide",
            "description": "Best practices for creating effective prompts for video generation with Amazon Nova Reel",
            "model": "amazon.nova-reel-v1:1",
            "supported_durations": "12-120 seconds (multiples of 6)",
            "supported_dimensions": ["1280x720", "1920x1080", "1024x1024"]
        },
        
        "basic_principles": {
            "be_specific": {
                "description": "Use specific, descriptive language rather than vague terms",
                "good_example": "A red cardinal perched on a snow-covered pine branch, morning sunlight filtering through the trees",
                "bad_example": "A bird on a tree"
            },
            "use_active_language": {
                "description": "Use active voice and present tense for dynamic scenes",
                "good_example": "The waves crash against the rocky shore as seagulls soar overhead",
                "bad_example": "Waves were crashing and birds were flying"
            },
            "include_context": {
                "description": "Provide environmental and atmospheric details",
                "good_example": "In a bustling Tokyo street at night, neon signs reflect on wet pavement as people hurry past",
                "bad_example": "People walking in a city"
            }
        },
        
        "video_structure": {
            "beginning_middle_end": {
                "description": "Structure your prompt with a clear progression",
                "example": "A butterfly lands on a flower (beginning), slowly opens and closes its wings (middle), then flies away into the sunset (end)",
                "tip": "For longer videos, describe multiple scenes or actions in sequence"
            },
            "pacing": {
                "description": "Consider the pacing of actions for your video duration",
                "short_videos": "Focus on single actions or moments (12-24 seconds)",
                "medium_videos": "Include 2-3 distinct actions or scene changes (30-60 seconds)",
                "long_videos": "Develop a narrative with multiple scenes (60-120 seconds)"
            }
        },
        
        "camera_control": {
            "overview": "Use specific camera terminology to control shot composition and movement",
            
            "shot_types": {
                "close_up": "Close-up shot of a person's face showing detailed expressions",
                "medium_shot": "Medium shot showing a person from waist up",
                "wide_shot": "Wide shot establishing the entire scene and environment",
                "extreme_close_up": "Extreme close-up focusing on eyes or hands",
                "establishing_shot": "Establishing shot revealing the location and setting"
            },
            
            "camera_movements": {
                "pan": "Camera pans left/right across the landscape",
                "tilt": "Camera tilts up to reveal the towering mountain",
                "zoom": "Camera slowly zooms in on the subject's face",
                "dolly": "Camera dollies forward through the forest path",
                "tracking": "Camera tracks alongside the running athlete",
                "crane": "Camera cranes up to show the aerial view of the city"
            },
            
            "angles": {
                "low_angle": "Low angle shot looking up at the imposing building",
                "high_angle": "High angle shot looking down at the busy street",
                "bird_eye": "Bird's eye view of the circular plaza",
                "worm_eye": "Worm's eye view of the towering trees",
                "dutch_angle": "Dutch angle creating a sense of unease"
            },
            
            "depth_of_field": {
                "shallow": "Shallow depth of field with blurred background",
                "deep": "Deep focus keeping both foreground and background sharp",
                "rack_focus": "Rack focus shifting from foreground to background"
            }
        },
        
        "lighting_and_atmosphere": {
            "natural_lighting": {
                "golden_hour": "Warm golden hour lighting casting long shadows",
                "blue_hour": "Soft blue hour twilight with city lights beginning to glow",
                "harsh_sunlight": "Bright midday sun creating strong contrasts",
                "overcast": "Soft, diffused lighting from overcast sky"
            },
            
            "artificial_lighting": {
                "neon": "Colorful neon lights reflecting on wet streets",
                "candlelight": "Warm, flickering candlelight creating intimate atmosphere",
                "spotlight": "Dramatic spotlight illuminating the performer",
                "backlighting": "Strong backlighting creating silhouettes"
            },
            
            "weather_atmosphere": {
                "fog": "Mysterious fog rolling through the valley",
                "rain": "Heavy rain creating ripples in puddles",
                "snow": "Gentle snowfall in the quiet forest",
                "storm": "Dramatic storm clouds gathering overhead"
            }
        },
        
        "subject_and_action": {
            "people": {
                "emotions": "Include specific emotions and expressions",
                "clothing": "Describe clothing style and colors",
                "age_appearance": "Specify age range and general appearance",
                "actions": "Use specific action verbs (strolling, sprinting, gesturing)"
            },
            
            "animals": {
                "species": "Be specific about animal species and breeds",
                "behavior": "Describe natural behaviors and movements",
                "habitat": "Include appropriate natural habitat details"
            },
            
            "objects": {
                "materials": "Specify materials (wooden, metallic, glass, fabric)",
                "condition": "Describe condition (new, weathered, antique, modern)",
                "interaction": "How objects interact with environment or subjects"
            }
        },
        
        "style_and_genre": {
            "cinematic_styles": {
                "documentary": "Documentary style with natural, observational camera work",
                "commercial": "Polished commercial style with perfect lighting",
                "indie_film": "Indie film aesthetic with handheld camera movement",
                "music_video": "Dynamic music video style with quick cuts and effects"
            },
            
            "visual_styles": {
                "realistic": "Photorealistic style with natural colors and lighting",
                "stylized": "Stylized with enhanced colors and dramatic lighting",
                "vintage": "Vintage film look with grain and muted colors",
                "modern": "Clean, modern aesthetic with sharp details"
            }
        },
        
        "technical_considerations": {
            "frame_rate": {
                "24fps": "Standard cinematic frame rate for natural motion",
                "higher_fps": "Higher frame rates for smooth slow-motion effects"
            },
            
            "resolution": {
                "1280x720": "HD resolution suitable for most applications",
                "1920x1080": "Full HD for higher quality output",
                "1024x1024": "Square format for social media"
            },
            
            "duration_planning": {
                "12_seconds": "Perfect for single action or moment",
                "24_seconds": "Good for simple scene with beginning and end",
                "60_seconds": "Allows for multiple actions or scene progression",
                "120_seconds": "Full narrative with multiple scenes possible"
            }
        },
        
        "example_prompts": {
            "nature": {
                "short": "Close-up of morning dew drops on a spider web, with soft sunrise lighting creating rainbow reflections",
                "medium": "A majestic eagle soars over a mountain valley, camera tracking its flight as it circles above a pristine lake, then dives toward the water",
                "long": "Time-lapse of a flower blooming in a meadow: starting as a bud at dawn, slowly opening petals as the sun rises, bees visiting throughout the day, and closing as sunset approaches"
            },
            
            "urban": {
                "short": "Neon signs reflecting in rain puddles on a busy Tokyo street at night, with people's feet splashing through the colorful reflections",
                "medium": "A street musician plays violin in a subway station, commuters pause to listen, coins drop into his case, camera slowly pulls back to reveal the bustling underground scene",
                "long": "Morning rush hour in Manhattan: alarm clocks ring, people emerge from apartments, flood the sidewalks, enter subway stations, trains arrive and depart, finally arriving at office buildings as the city comes alive"
            },
            
            "portrait": {
                "short": "Extreme close-up of an elderly craftsman's weathered hands carving intricate details into wood, with warm workshop lighting",
                "medium": "A young dancer practices alone in a sunlit studio, her movements flowing from gentle stretches to powerful leaps, shadows dancing on the wooden floor",
                "long": "Portrait of a chef preparing a signature dish: selecting fresh ingredients at market, returning to kitchen, methodically preparing each component, plating with artistic precision, and presenting the finished masterpiece"
            }
        },
        
        "common_mistakes": {
            "too_vague": {
                "problem": "Prompts that are too general or vague",
                "example": "A person doing something",
                "solution": "Be specific about who, what, where, when, and how"
            },
            
            "conflicting_elements": {
                "problem": "Including contradictory or impossible elements",
                "example": "Underwater scene with fire burning",
                "solution": "Ensure all elements are physically and logically consistent"
            },
            
            "overcomplication": {
                "problem": "Trying to include too many elements or actions",
                "example": "A person cooking while dancing while painting while talking on phone",
                "solution": "Focus on 1-3 main elements or actions for clarity"
            },
            
            "inappropriate_duration": {
                "problem": "Describing actions that don't match video duration",
                "example": "Describing a 5-minute cooking process for a 12-second video",
                "solution": "Match action complexity to video duration"
            }
        },
        
        "optimization_tips": {
            "use_keywords": "Include relevant keywords for style, mood, and technical aspects",
            "specify_quality": "Add terms like 'high quality', 'detailed', 'professional' for better results",
            "mention_equipment": "Reference camera types or lenses for specific looks (e.g., 'shot with 85mm lens')",
            "include_mood": "Describe the emotional tone or atmosphere you want to convey",
            "test_variations": "Try different phrasings of the same concept to find what works best"
        },
        
        "prompt_templates": {
            "basic_template": "[Subject] [Action] [Location] [Lighting] [Camera angle] [Style]",
            "narrative_template": "[Opening scene], [transition/development], [conclusion/resolution]",
            "technical_template": "[Shot type] of [subject] [action] in [environment], [lighting], [camera movement], [style]"
        }
    }
