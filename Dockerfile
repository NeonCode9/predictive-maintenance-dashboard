#Use the official Python 3.9 slim image for a lightweight container

FROM python:3.9-slim

#Set the working directory inside the container

WORKDIR /app

#Copy the requirements file first to leverage Docker cache

COPY requirements.txt .

#Install dependencies (no-cache-dir keeps the container size small)

RUN pip install --no-cache-dir -r requirements.txt

#Copy the rest of your application code into the container

COPY . .

#Expose port 7860, which is the standard port required by Hugging Face Spaces

EXPOSE 7860

#Command to run the Streamlit application

Change 'streamlit_app.py' if your main python file is named differently (e.g., 'app.py')

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=7860", "--server.address=0.0.0.0"]