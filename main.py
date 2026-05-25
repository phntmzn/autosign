#!/usr/bin/env python3
"""
SoundCloud Account Creator & Comment Bot - FIXED VERSION
"""

import subprocess
import sys
import time
import random
from faker import Faker

# ============================================
# INSTALL MISSING PACKAGES
# ============================================

def install_packages():
    """Install required packages if missing"""
    packages = ['playwright', 'faker']
    
    for package in packages:
        try:
            __import__(package)
            print(f"✓ {package} already installed")
        except ImportError:
            print(f"📦 Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    # Install playwright browser
    print("📦 Installing Chromium browser...")
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])

install_packages()

# Now import properly
from playwright.sync_api import sync_playwright

# ============================================
# FIXED ACCOUNT CREATION
# ============================================

def create_fake_accounts():
    """Generate fake email/password pairs"""
    fake = Faker()
    
    accounts = {}
    for i in range(10):
        accounts[i] = {
            'email': fake.email(),
            'password': fake.password(length=12)
        }
    
    print("\n📧 Generated Accounts:")
    for idx, acc in accounts.items():
        print(f"  Account {idx}: {acc['email']} / {acc['password']}")
    
    return accounts

def attempt_signup(page, email, password):
    """Attempt to create a SoundCloud account (likely to fail without SMS verification)"""
    print(f"\n📝 Attempting to create account: {email}")
    
    try:
        # Go to signup page
        page.goto('https://soundcloud.com/signup', timeout=30000)
        time.sleep(random.uniform(2, 3))
        
        # Click "Create account" or email signup option
        try:
            email_btn = page.wait_for_selector('button:has-text("Email"), button[aria-label="Sign up with email"]', timeout=5000)
            email_btn.click()
            time.sleep(1)
        except:
            pass
        
        # Fill email
        email_input = page.wait_for_selector('input[name="email"], input[type="email"]', timeout=10000)
        email_input.fill(email)
        time.sleep(random.uniform(0.5, 1))
        
        # Fill password
        pass_input = page.wait_for_selector('input[name="password"], input[type="password"]', timeout=5000)
        pass_input.fill(password)
        time.sleep(random.uniform(0.5, 1))
        
        # Fill display name
        try:
            name_input = page.wait_for_selector('input[name="display_name"]', timeout=3000)
            fake = Faker()
            name_input.fill(fake.name())
        except:
            pass
        
        # Click sign up button
        signup_btn = page.wait_for_selector('button[type="submit"]:has-text("Sign up"), button:has-text("Create account")', timeout=5000)
        signup_btn.click()
        
        # Wait for response
        time.sleep(3)
        
        # Check if verification required
        if "verify" in page.url or "captcha" in page.url:
            print(f"⚠️ Account {email} requires verification (captcha/SMS)")
            return False
        
        print(f"✅ Account created: {email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create {email}: {e}")
        return False

# ============================================
# FIXED COMMENT BOT
# ============================================

def post_comments_on_tracks(track_urls, comment_text, num_comments=30):
    """Post comments on SoundCloud tracks"""
    
    comments_posted = 0
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)  # Set to True for invisible mode
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()
        
        print("\n💬 Starting comment bot...")
        
        for url in track_urls:
            if comments_posted >= num_comments:
                break
                
            try:
                print(f"\n🎵 Processing: {url.split('/')[-1]}")
                
                # Navigate to track
                page.goto(url, timeout=30000)
                page.wait_for_load_state('networkidle')
                time.sleep(random.uniform(2, 4))
                
                # Scroll to comments section
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)
                
                # Find comment input and post
                comment_selectors = [
                    'textarea[placeholder*="comment"]',
                    'textarea[placeholder*="Comment"]',
                    '[contenteditable="true"][role="textbox"]',
                    '.commentInput__textarea',
                    'div[data-testid="comment-input"] textarea'
                ]
                
                comment_posted = False
                
                for selector in comment_selectors:
                    try:
                        # Find comment input
                        comment_input = page.wait_for_selector(selector, timeout=3000)
                        if comment_input and comment_input.is_visible():
                            # Click to focus
                            comment_input.click()
                            time.sleep(0.5)
                            
                            # Type comment
                            comment_input.fill(comment_text)
                            time.sleep(random.uniform(0.5, 1))
                            
                            # Post comment
                            post_selectors = [
                                'button:has-text("Post")',
                                'button:has-text("Comment")',
                                'button[type="submit"]',
                                'button.submitButton'
                            ]
                            
                            for post_btn in post_selectors:
                                try:
                                    button = page.wait_for_selector(post_btn, timeout=2000)
                                    if button:
                                        button.click()
                                        comment_posted = True
                                        break
                                except:
                                    continue
                            
                            if comment_posted:
                                break
                    except:
                        continue
                
                if comment_posted:
                    comments_posted += 1
                    print(f"✅ Comment {comments_posted}/{num_comments} posted!")
                else:
                    print("❌ Could not post comment - might need login")
                
                # Random delay between comments
                delay = random.randint(30, 90)
                print(f"💤 Waiting {delay}s before next comment...")
                time.sleep(delay)
                
            except Exception as e:
                print(f"❌ Error on track: {e}")
                continue
        
        print(f"\n📊 Complete! Posted {comments_posted} comments")
        browser.close()

# ============================================
# FIXED API CALL (SoundCloud requires auth)
# ============================================

def api_call_example():
    """Example of proper API call (requires authentication)"""
    print("\n🔑 Note: SoundCloud API requires authentication")
    print("You need to get client_id or use OAuth first")
    
    # This is just an example - won't work without auth
    # Real implementation would need:
    # 1. Get client_id from SoundCloud
    # 2. Use OAuth token
    # 3. Make authenticated requests
    
    print("\n📡 API Example (won't work without auth):")
    print("POST https://api-v2.soundcloud.com/users")
    print("Headers: {'Authorization': 'Bearer YOUR_TOKEN'}")
    print("Body: {'email': '...', 'password': '...'}")

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    print("\n" + "="*60)
    print("🎵 SOUNDCLOUD BOT - FIXED VERSION")
    print("="*60)
    
    # 1. Generate fake accounts
    accounts = create_fake_accounts()
    
    # 2. API example (won't work without auth)
    api_call_example()
    
    # 3. Comment bot example
    print("\n" + "="*60)
    print("💬 COMMENT BOT")
    print("="*60)
    
    # Replace with actual SoundCloud track URLs
    track_urls = [
        "https://soundcloud.com/artist/your-track-1",  # REPLACE THESE
        "https://soundcloud.com/artist/your-track-2",  # WITH REAL URLs
    ]
    
    comment_text = "🔥 Great track!"
    
    # Ask user if they want to run comment bot
    try:
        run_comments = input("\nRun comment bot? (y/n): ").lower()
        if run_comments == 'y':
            if track_urls[0] == "https://soundcloud.com/artist/your-track-1":
                print("\n⚠️ WARNING: You need to edit track_urls with actual SoundCloud URLs!")
                print("Edit the script and add real track URLs before running.")
            else:
                num_comments = int(input("How many comments to post? (max 30): ") or "30")
                post_comments_on_tracks(track_urls, comment_text, min(num_comments, 30))
    except KeyboardInterrupt:
        print("\n\n⚠️ Stopped by user")
    
    print("\n✅ Done!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
