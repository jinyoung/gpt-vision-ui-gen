from openai import OpenAI
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from fastapi.responses import RedirectResponse

app = FastAPI()

# 정적 파일(예: HTML, CSS, JS)을 제공하기 위한 디렉토리 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

client = OpenAI()

@app.get("/")
async def root():
    return RedirectResponse(url='/static/index.html')

@app.post("/process-image")
async def create_upload_file(request: Request):
    # JSON 요청 본문을 파싱합니다.
    body = await request.json()
    imageInput = body.get("image_base64")
    

    response = create_html_from_image(imageInput)
    async with aiofiles.open("result.html", 'w') as html_file:
        await html_file.write(response)

    return {"filename": file.filename}


def create_html_from_image(imageInput: str):
  client = OpenAI()

  response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    max_tokens = 4096,
    temperature = 0,

    messages=[
      {'role': 'system', 'content': '\nYou are an expert Tailwind developer\nYou take screenshots of a reference web page from the user, and then build single page apps \nusing Tailwind, HTML and JS.\nYou might also be given a screenshot(The second image) of a web page that you have already built, and asked to\nupdate it to look more like the reference image(The first image).\n\n- Make sure the app looks exactly like the screenshot.\n- Pay close attention to background color, text color, font size, font family, \npadding, margin, border, etc. Match the colors and sizes exactly.\n- Use the exact text from the screenshot.\n- Do not add comments in the code such as "<!-- Add other navigation links as needed -->" and "<!-- ... other news items ... -->" in place of writing the full code. WRITE THE FULL CODE.\n- Repeat elements as needed to match the screenshot. For example, if there are 15 items, the code should have 15 items. DO NOT LEAVE comments like "<!-- Repeat for each news item -->" or bad things will happen.\n- For images, use placeholder images from https://placehold.co and include a detailed description of the image in the alt text so that an image generation AI can generate the image later.\n\nIn terms of libraries,\n\n- Use this script to include Tailwind: <script src="https://cdn.tailwindcss.com"></script>\n- You can use Google Fonts\n- Font Awesome for icons: <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"></link>\n\nReturn only the full code in <html></html> tags.\nDo not include markdown "```" or "```html" at the start or end.\n'},
      {
        "role": "user",
        "content": [        
          {
            "type": "image_url",
            "image_url": {
              "url": f"{imageInput}",
              'detail': 'high'}
          }
          , 
          {'type': 'text', 'text': '\nGenerate code for a web page that looks exactly like this.\n'}
        ],
      }
    ],

  )

  return (response.choices[0].message.content)


import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


# with open('result.html', 'w') as file:
#     file.write(response.choices[0].message.content)
