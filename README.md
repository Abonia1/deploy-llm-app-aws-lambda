
# LLM Application on AWS Lambda 🚀

This project demonstrates how to deploy a **LangChain-based application** on **AWS Lambda**. The app leverages OpenAI's GPT model, web scraping, and document retrieval to provide intelligent responses based on content from a specific blog. 

---

## ✨ Features

- 🛠️ **Serverless Deployment**: Runs in AWS Lambda for scalability and cost-effectiveness.
- 🌐 **Web Scraping**: Dynamically extracts and processes content from web pages.
- 🧠 **Smart Document Retrieval**: Uses **Chroma** for efficient indexing and retrieval.
- 💬 **OpenAI GPT Integration**: Provides contextual responses using **GPT-3.5-turbo**.
- 🔒 **Secure Configuration**: Manages API keys securely via environment variables.


---

## Project Structure

- **`load_data()`**: Scrapes and prepares the data for indexing.
- **`get_response(query)`**: Retrieves relevant content and generates an LLM-based response.
- **`lambda_handler(event, context)`**: AWS Lambda handler to process incoming requests and return responses.

---

## Requirements

### AWS Setup
- **AWS Lambda**: Ensure you have permissions to create and deploy Lambda functions.
- **IAM Role**: Attach permissions for the Lambda function to access environment variables and other necessary AWS resources.

### Python Dependencies
The following libraries are required:
- `boto3`
- `bs4`
- `langchain`
- `langchain_community`
- `langchain_core`
- `langchain_text_splitters`
- `os`

Install them locally using:
```bash
pip install boto3 bs4 langchain langchain-community langchain-core langchain-text-splitters
```

---

## Environment Variables

Set the `OPENAI_API_KEY` in the Lambda function’s environment variables:
1. Navigate to your Lambda function in AWS Console.
2. Go to **Configuration > Environment Variables**.
3. Add a key-value pair:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key.

---

## Deployment Steps

1. **Package the Application**:
   - Create a deployment package with all required dependencies and the application script:
     ```bash
     zip -r deploy_package.zip .
     ```

2. **Upload to Lambda**:
   - Log in to the AWS Console.
   - Create a new Lambda function or update an existing one.
   - Upload the `deploy_package.zip` file.

3. **Configure Lambda**:
   - Set the runtime to **Python 3.9** or higher.
   - Add the `OPENAI_API_KEY` in **Environment Variables**.

4. **Test the Function**:
   - Use the test event format below to invoke the Lambda function:
     ```json
     {
       "question": "What is the main purpose of the blog?"
     }
     ```

---

## How It Works

1. **Data Loading**: The `load_data()` function scrapes content from the blog, splits it into manageable chunks, and indexes it using Chroma.
2. **Retrieval and Response**:
   - The app retrieves relevant content based on the query.
   - It formats the content and passes it through a LangChain RAG (Retrieve and Generate) chain.
3. **Output**: The result is returned as a JSON response to the caller.

---

## Example Query

Input:
```json
{
  "question": "What are autonomous agents in AI?"
}
```

Output:
```json
{
  "body": "Autonomous agents are systems that can independently make decisions and act on them without human intervention, typically leveraging AI models.",
  "statusCode": 200
}
```

---

## Troubleshooting

- **Missing Dependencies**: Ensure all dependencies are included in the deployment package.
- **Invalid API Key**: Verify the `OPENAI_API_KEY` is correctly set in the environment variables.
- **Lambda Timeouts**: Increase the timeout duration in the Lambda configuration if the function takes too long to execute.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
```
 
