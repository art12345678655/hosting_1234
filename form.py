from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import shutil
import json
from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories
os.makedirs("static", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Create necessary HTML, CSS and JS files if they don't exist
def create_files():
    # HTML content
    html_content = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Яндекс Афиша Form</title>
    <link rel="stylesheet" href="/static/styles.css">
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body>
    <div class="container">
        <h1>Яндекс Афиша Form</h1>
        
        <form id="eventForm">
           
            
            <div class="event-sections" id="eventSections">
                <!-- Initial event section -->
                <div class="event-section" data-section-id="1">
                    <h2>Событие, на котором нужно изменить контент 1</h2>
                    
                    <div class="form-group">
                        <label for="title1">Название и дата *</label>
                        <input type="text" id="title1" name="title1" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="link1">Ссылка на событие на Яндекс Афише</label>
                        <input type="text" id="link1" name="link1">
                    </div>
                    
                    <div class="form-group">
                        <label for="description1">Текстовое описание</label>
                        <textarea id="description1" name="description1" rows="5"></textarea>
                        <button type="button" class="improve-btn" data-for="description1">Улучшить текст</button>
                        
                        <div class="improvement-box" id="improvement-box-description1" style="display: none;">
                            <h4>Предложенный вариант:</h4>
                            <div class="improved-text" id="improved-description1"></div>
                            <div class="action-btns">
                                <button type="button" class="accept-btn" data-for="description1">Принять предложение</button>
                                <button type="button" class="decline-btn" data-for="description1">Отклонить предложение</button>
                            </div>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label for="images1">Изображение, которое может иллюстрировать событие (до 5 файлов, макс. 9MB каждый)</label>
                        <input type="file" id="images1" name="images1" multiple accept="image/*">
                        <p class="file-guidelines">Рекомендации: изображения должны быть четкими, высокого качества и относиться к событию.</p>
                    </div>
                    
                    <div class="form-group">
                        <label for="textFiles1">Файлы с описанием (до 5 файлов, макс. 9MB каждый)</label>
                        <input type="file" id="textFiles1" name="textFiles1" multiple>
                    </div>
                    
                    <div class="form-group">
                        <label for="source1">Источник описания и изображений *</label>
                        <input type="text" id="source1" name="source1" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="childrenTerms1">Условия посещения события с детьми</label>
                        <textarea id="childrenTerms1" name="childrenTerms1" rows="3"></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="message1">Сообщение</label>
                        <textarea id="message1" name="message1" rows="3"></textarea>
                    </div>
                </div>
            </div>
            
            <button type="button" id="addMoreBtn" class="add-more-btn">+ Ещё</button>
            
            <button type="submit" id="submitBtn" class="submit-btn">Отправить</button>
        </form>
    </div>

    <script src="/static/script.js"></script>
</body>
</html>
    """
    
    # CSS content
    css_content = """
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f5f5;
    padding: 20px;
}

/* Telegram theme integration */
body.dark {
    color: #fff;
    background-color: #212121;
}

body.dark .container {
    background-color: #333;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

body.dark h1, body.dark h2 {
    color: #fff;
}

body.dark .event-section {
    background-color: #424242;
    border-left: 4px solid #4eadf3;
}

body.dark input[type="text"], 
body.dark textarea {
    background-color: #555;
    color: #fff;
    border: 1px solid #777;
}

body.dark .radio-group {
    background-color: #424242;
}

body.dark .improvement-box {
    background-color: #3a5147;
    border: 1px solid #4a7263;
}

body.dark .improved-text {
    background-color: #555;
    color: #fff;
    border: 1px solid #777;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
    text-align: center;
    margin-bottom: 20px;
    color: #333;
}

h2 {
    margin: 15px 0;
    font-size: 18px;
    color: #2c3e50;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
}

.radio-group {
    margin-bottom: 20px;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 6px;
}

.radio-group label {
    display: block;
    margin-bottom: 10px;
    font-weight: 500;
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
}

input[type="text"], 
textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
}

textarea {
    resize: vertical;
}

input[type="file"] {
    padding: 10px 0;
}

.file-guidelines {
    font-size: 12px;
    color: #666;
    margin-top: 5px;
}

.event-section {
    margin-bottom: 30px;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    border-left: 4px solid #3498db;
}

.add-more-btn {
    background-color: #ecf0f1;
    color: #3498db;
    border: 2px solid #3498db;
    padding: 10px 20px;
    font-weight: bold;
    border-radius: 4px;
    cursor: pointer;
    margin: 20px 0;
    display: block;
    width: 100%;
}

.add-more-btn:hover {
    background-color: #e8f4f8;
}

.submit-btn {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 12px 20px;
    font-weight: bold;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 20px;
    display: block;
    width: 100%;
    font-size: 16px;
}

.submit-btn:hover {
    background-color: #2980b9;
}

.improve-btn {
    background-color: #2ecc71;
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 5px;
    font-size: 14px;
}

.improve-btn:hover {
    background-color: #27ae60;
}

.improvement-box {
    margin-top: 15px;
    padding: 15px;
    background-color: #f1f9f6;
    border: 1px solid #d4e9e2;
    border-radius: 6px;
}

.improved-text {
    padding: 10px;
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-bottom: 10px;
    min-height: 80px;
}

.action-btns {
    display: flex;
    gap: 10px;
}

.accept-btn, .decline-btn {
    padding: 8px 15px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    flex: 1;
}

.accept-btn {
    background-color: #2ecc71;
    color: white;
    border: none;
}

.accept-btn:hover {
    background-color: #27ae60;
}

.decline-btn {
    background-color: #e74c3c;
    color: white;
    border: none;
}

.decline-btn:hover {
    background-color: #c0392b;
}



/* Add these styles to the CSS content */

.thank-you-message {
    text-align: center;
    padding: 30px;
    background-color: #f9f9f9;
    border-radius: 8px;
    margin: 20px 0;
    border-left: 4px solid #2ecc71;
}

body.dark .thank-you-message {
    background-color: #424242;
    border-left: 4px solid #2ecc71;
}

.thank-you-message h2 {
    color: #2ecc71;
    margin-bottom: 15px;
    border-bottom: none;
}

body.dark .thank-you-message h2 {
    color: #4ce69c;
}

.thank-you-message p {
    margin-bottom: 20px;
    font-size: 16px;
}

.submit-again-btn {
    background-color: #2ecc71;
    color: white;
    border: none;
    padding: 12px 20px;
    font-weight: bold;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
}

.submit-again-btn:hover {
    background-color: #27ae60;
}

    """
    
    # JS content
    js_content = """
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Telegram WebApp
    const tgApp = window.Telegram.WebApp;
    tgApp.expand();
    
    // Set theme based on Telegram
    document.body.className = tgApp.colorScheme;
    
    // Get user data from Telegram
    const initData = tgApp.initData || '';
    const initDataUnsafe = tgApp.initDataUnsafe || {};
    const user = initDataUnsafe.user || {};
    
    console.log('Telegram WebApp initialized', { user });
    
    let sectionCount = 1;
    const eventSectionsContainer = document.getElementById('eventSections');
    const addMoreBtn = document.getElementById('addMoreBtn');
    const form = document.getElementById('eventForm');
    const container = document.querySelector('.container');
    
    // Create thank you message and reset button elements (hidden initially)
    const thankYouDiv = document.createElement('div');
    thankYouDiv.className = 'thank-you-message';
    thankYouDiv.style.display = 'none';
    thankYouDiv.innerHTML = `
        <h2>Спасибо за отправку!</h2>
        <p>Ваша форма была успешно отправлена.</p>
        <button id="submitAgainBtn" class="submit-again-btn">Отправить еще раз</button>
    `;
    container.appendChild(thankYouDiv);
    
    // Add event listener to the submit again button
    document.getElementById('submitAgainBtn').addEventListener('click', function() {
        // Hide thank you message and show form again
        thankYouDiv.style.display = 'none';
        form.style.display = 'block';
        
        // Reset the form
        form.reset();
        
        // Remove all additional sections, keeping only the first one
        const sections = document.querySelectorAll('.event-section');
        for (let i = 1; i < sections.length; i++) {
            sections[i].remove();
        }
        
        // Reset section count
        sectionCount = 1;
    });
    
    // Add more sections
    addMoreBtn.addEventListener('click', function() {
        sectionCount++;
        const newSection = createNewSection(sectionCount);
        eventSectionsContainer.appendChild(newSection);
        
        // Add event listeners to the new improve buttons
        const improveBtn = newSection.querySelector('.improve-btn');
        improveBtn.addEventListener('click', handleImproveText);
        
        // Add event listeners to accept and decline buttons
        const acceptBtn = newSection.querySelector('.accept-btn');
        const declineBtn = newSection.querySelector('.decline-btn');
        acceptBtn.addEventListener('click', handleAcceptImprovement);
        declineBtn.addEventListener('click', handleDeclineImprovement);
    });
    
    // Add event listeners to initial improve buttons
    document.querySelectorAll('.improve-btn').forEach(btn => {
        btn.addEventListener('click', handleImproveText);
    });
    
    // Add event listeners to initial accept and decline buttons
    document.querySelectorAll('.accept-btn').forEach(btn => {
        btn.addEventListener('click', handleAcceptImprovement);
    });
    
    document.querySelectorAll('.decline-btn').forEach(btn => {
        btn.addEventListener('click', handleDeclineImprovement);
    });
    
    // Form submit
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Create FormData object
        const formData = new FormData(form);
        
        // Collect all form data
        const formDataObj = {};
        formData.forEach((value, key) => {
            // Skip file inputs for now as they require special handling
            if (!key.startsWith('images') && !key.startsWith('textFiles')) {
                formDataObj[key] = value;
            }
        });
        
        // Add user information from Telegram if available
        if (user) {
            formDataObj.user = {
                id: user.id || '',
                first_name: user.first_name || '',
                last_name: user.last_name || '',
                username: user.username || ''
            };
        }
        
        // Add timestamp
        formDataObj.submission_time = new Date().toISOString();
        
        // Log form data
        console.log('Form submission:', formDataObj);
        
        try {
            // Send to backend to save to JSON file
            const response = await fetch('/api/submit-form', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formDataObj),
            });
            
            if (!response.ok) {
                throw new Error('Failed to submit form');
            }
            
            const result = await response.json();
            console.log('Form saved:', result);
            
            // Send data to Telegram WebApp
            tgApp.sendData(JSON.stringify(formDataObj));
            
            // Hide form and show thank you message
            form.style.display = 'none';
            thankYouDiv.style.display = 'block';
            
            // Scroll to top
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
            
        } catch (error) {
            console.error('Error submitting form:', error);
            
            // Show error message
            tgApp.showPopup({
                title: "Error",
                message: "Failed to submit form. Please try again.",
                buttons: [{type: "ok"}]
            });
        }
    });
    
    // Function to handle text improvement request
    async function handleImproveText(e) {
        const textareaId = e.target.getAttribute('data-for');
        const textarea = document.getElementById(textareaId);
        const originalText = textarea.value;
        
        if (!originalText.trim()) {
            tgApp.showPopup({
                title: "Warning",
                message: "Please enter some text before requesting improvement.",
                buttons: [{type: "ok"}]
            });
            return;
        }
        
        // Show loading state
        e.target.textContent = 'Улучшаем...';
        e.target.disabled = true;
        
        try {
            // Send text to backend for improvement
            const response = await fetch('/api/improve-text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: originalText }),
            });
            
            if (!response.ok) {
                throw new Error('Failed to improve text');
            }
            
            const data = await response.json();
            
            // Show improvement box with improved text
            const improvementBox = document.getElementById(`improvement-box-${textareaId}`);
            const improvedTextElement = document.getElementById(`improved-${textareaId}`);
            
            improvedTextElement.textContent = data.improved_text;
            improvementBox.style.display = 'block';
            
        } catch (error) {
            console.error('Error improving text:', error);
            
            // Fallback for demo - simulate improved text
            const improvedText = simulateImprovedText(originalText);
            
            // Show improvement box with fallback improved text
            const improvementBox = document.getElementById(`improvement-box-${textareaId}`);
            const improvedTextElement = document.getElementById(`improved-${textareaId}`);
            
            improvedTextElement.textContent = improvedText;
            improvementBox.style.display = 'block';
        } finally {
            // Reset button state
            e.target.textContent = 'Улучшить текст';
            e.target.disabled = false;
        }
    }
    
    // Function to handle accepting text improvement
    function handleAcceptImprovement(e) {
        const textareaId = e.target.getAttribute('data-for');
        const textarea = document.getElementById(textareaId);
        const improvedText = document.getElementById(`improved-${textareaId}`).textContent;
        
        // Replace original text with improved text
        textarea.value = improvedText;
        
        // Hide improvement box
        document.getElementById(`improvement-box-${textareaId}`).style.display = 'none';
    }
    
    // Function to handle declining text improvement
    function handleDeclineImprovement(e) {
        const textareaId = e.target.getAttribute('data-for');
        
        // Hide improvement box
        document.getElementById(`improvement-box-${textareaId}`).style.display = 'none';
    }
    
    // Function to create a new section
    function createNewSection(sectionNumber) {
        const sectionDiv = document.createElement('div');
        sectionDiv.className = 'event-section';
        sectionDiv.dataset.sectionId = sectionNumber;
        
        sectionDiv.innerHTML = `
            <h2>Событие, на котором нужно изменить контент ${sectionNumber}</h2>
            
            <div class="form-group">
                <label for="title${sectionNumber}">Название и дата *</label>
                <input type="text" id="title${sectionNumber}" name="title${sectionNumber}" required>
            </div>
            
            <div class="form-group">
                <label for="link${sectionNumber}">Ссылка на событие на Яндекс Афише</label>
                <input type="text" id="link${sectionNumber}" name="link${sectionNumber}">
            </div>
            
            <div class="form-group">
                <label for="description${sectionNumber}">Текстовое описание</label>
                <textarea id="description${sectionNumber}" name="description${sectionNumber}" rows="5"></textarea>
                <button type="button" class="improve-btn" data-for="description${sectionNumber}">Улучшить текст</button>
                
                <div class="improvement-box" id="improvement-box-description${sectionNumber}" style="display: none;">
                    <h4>Предложенный вариант:</h4>
                    <div class="improved-text" id="improved-description${sectionNumber}"></div>
                    <div class="action-btns">
                        <button type="button" class="accept-btn" data-for="description${sectionNumber}">Принять предложение</button>
                        <button type="button" class="decline-btn" data-for="description${sectionNumber}">Отклонить предложение</button>
                    </div>
                </div>
            </div>
            
            <div class="form-group">
                <label for="images${sectionNumber}">Изображение, которое может иллюстрировать событие (до 5 файлов, макс. 9MB каждый)</label>
                <input type="file" id="images${sectionNumber}" name="images${sectionNumber}" multiple accept="image/*">
                <p class="file-guidelines">Рекомендации: изображения должны быть четкими, высокого качества и относиться к событию.</p>
            </div>
            
            <div class="form-group">
                <label for="textFiles${sectionNumber}">Файлы с описанием (до 5 файлов, макс. 9MB каждый)</label>
                <input type="file" id="textFiles${sectionNumber}" name="textFiles${sectionNumber}" multiple>
            </div>
            
            <div class="form-group">
                <label for="source${sectionNumber}">Источник описания и изображений *</label>
                <input type="text" id="source${sectionNumber}" name="source${sectionNumber}" required>
            </div>
            
            <div class="form-group">
                <label for="childrenTerms${sectionNumber}">Условия посещения события с детьми</label>
                <textarea id="childrenTerms${sectionNumber}" name="childrenTerms${sectionNumber}" rows="3"></textarea>
            </div>
            
            <div class="form-group">
                <label for="message${sectionNumber}">Сообщение</label>
                <textarea id="message${sectionNumber}" name="message${sectionNumber}" rows="3"></textarea>
            </div>
        `;
        
        return sectionDiv;
    }
    
    // Fallback function to simulate improved text (when backend is not available)
    function simulateImprovedText(originalText) {
        // Simple simulation for demo purposes
        if (!originalText) return "";
        
        // Add some improvements to the text
        let improved = originalText.trim();
        
        // Capitalize first letter of each sentence
        improved = improved.replace(/([.!?]\\s+)([a-zа-яё])/g, (match, punctuation, letter) => {
            return punctuation + letter.toUpperCase();
        });
        
        // Ensure the first letter of the text is capitalized
        improved = improved.charAt(0).toUpperCase() + improved.slice(1);
        
        // Add some phrases to make it sound better
        if (improved.length < 100) {
            improved += " Это захватывающее событие обещает стать незабываемым для всех посетителей.";
        }
        
        // Replace some common words with more expressive ones
        improved = improved
            .replace(/хорошо/g, "превосходно")
            .replace(/интересно/g, "захватывающе")
            .replace(/важно/g, "исключительно важно");
            
        return improved;
    }
});

    """
    
    # Write the files
    with open("static/styles.css", "w", encoding="utf-8") as f:
        f.write(css_content)
    
    with open("static/script.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    
    return html_content

# Create the necessary files
html_content = create_files()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

class TextImproveRequest(BaseModel):
    text: str

class FormSubmissionRequest(BaseModel):
    user: Dict[str, Any] = None
    submission_time: str = None

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_content

@app.post("/api/improve-text")
async def improve_text(request: TextImproveRequest):
    try:
        original_text = request.text
        
        if not original_text:
            raise HTTPException(status_code=400, detail="No text provided")
        
        # Improve the text with a dummy function (placeholder for LLM integration)
        improved_text = improve_text_with_llm(original_text)
        
        return JSONResponse(content={"improved_text": improved_text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/submit-form")
async def submit_form(request: Request):
    try:
        form_data = await request.json()
        
        # Generate a timestamp-based filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_id = form_data.get("user", {}).get("id", "unknown")
        filename = f"logs/form_submission_{user_id}_{timestamp}.json"
        
        # Save to JSON file
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(form_data, f, ensure_ascii=False, indent=2)
        
        # Log to a common log file as well
        append_to_log(form_data)
        
        return JSONResponse(content={
            "status": "success", 
            "message": "Form data saved successfully",
            "filename": filename
        })
    except Exception as e:
        print(f"Error saving form data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def append_to_log(form_data: dict):
    """Append form submission to a common log file"""
    log_file = "logs/all_submissions.json"
    
    try:
        # Read existing logs
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
        else:
            logs = []
        
        # Append new submission
        logs.append(form_data)
        
        # Write back to file
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error appending to log file: {str(e)}")

def improve_text_with_llm(text: str) -> str:
    """
    Dummy function to simulate text improvement with an LLM.
    In a real application, this would call an actual LLM API.
    """
    if not text:
        return ""
    
    # Simple improvements for demonstration
    improved = text.strip()
    
    # Capitalize first letter of each sentence
    improved = '. '.join(s.capitalize() for s in improved.split('. '))
    
    # Ensure the first letter of the text is capitalized
    if improved:
        improved = improved[0].upper() + improved[1:]
    
    # Add some enhancements
    if len(improved) < 100:
        improved += " Это захватывающее событие обещает стать незабываемым для всех посетителей."
    
    # Replace some common words with more expressive ones
    replacements = {
        "хорошо": "превосходно",
        "интересно": "захватывающе",
        "важно": "исключительно важно",
        "событие": "мероприятие",
        "красивый": "великолепный",
        "большой": "масштабный"
    }
    
    for word, replacement in replacements.items():
        improved = improved.replace(word, replacement)
    
    # Add more structure if the text is long enough
    if len(improved) > 200:
        sentences = improved.split('. ')
        if len(sentences) > 3:
            # Group sentences into paragraphs
            paragraphs = []
            current_paragraph = []
            
            for i, sentence in enumerate(sentences):
                current_paragraph.append(sentence)
                if (i + 1) % 3 == 0 or i == len(sentences) - 1:
                    paragraphs.append('. '.join(current_paragraph) + '.')
                    current_paragraph = []
            
            improved = '\n\n'.join(paragraphs)
    
    return improved

@app.get("/logs")
async def get_logs():
    """API endpoint to retrieve logs (useful for debugging or admin purposes)"""
    try:
        log_file = "logs/all_submissions.json"
        if not os.path.exists(log_file):
            return JSONResponse(content={"logs": []})
            
        with open(log_file, "r", encoding="utf-8") as f:
            logs = json.load(f)
        
        return JSONResponse(content={"logs": logs})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
