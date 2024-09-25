from flask import Flask, request, jsonify
import uuid
import signal
import logging
from rag import rag
from utils.weaviate_client import initialize_weaviate_client, close_weaviate_client
# import db

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize Weaviate client globally
# weaviate_client = None

# @app.before_first_request
# def setup_weaviate_client():
#     global weaviate_client
#     initialize_weaviate_client()
#     print("Weaviate client initialize.")

# @app.teardown_appcontext
def teardown_weaviate_client(exception=None):
    close_weaviate_client()
    print("Weaviate client connection closed.")

def signal_handler(sig, frame):
    print("Received signal to terminate.")
    teardown_weaviate_client()  # Вызываем функцию закрытия клиента
    exit(0)  # Завершаем приложение

signal.signal(signal.SIGINT, signal_handler)

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    # Generate a conversation ID
    conversation_id = str(uuid.uuid4())
    
    try:
        answer_data = rag(question)
        print(f"Answer data: {answer_data}")    # Add this line to debug
        result = jsonify({
            'conversation_id': conversation_id,
            'question': question,
            'result': answer_data['answer'],
        })

        # db.save_conversation(
        #     conversation_id=conversation_id, 
        #     question=question, 
        #     answer_data = answer_data, 
        #     timestamp=None)
        
        return result
    
    except Exception as e:
        logging.error(f"Error processing question: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your question'}), 500

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    conversation_id = data.get('conversation_id')
    feedback = data.get('feedback')
    
    if not conversation_id or feedback not in [1, -1]:
        return jsonify({'error': 'Invalid input'}), 400
    
    # db.save_feedback(
    #     conversation_id=conversation_id,
    #     feedback=feedback,
    # )
    
    return jsonify({
        'message': 'Feedback received. Thank you!',
        'conversation_id': conversation_id,
        'feedback': feedback
    })

if __name__ == '__main__':
    try:
        app.run(debug=True, host="0.0.0.0", port=5000)
        weaviate_client = None
        weaviate_client = initialize_weaviate_client()
    except Exception as e:
        logging.error(f"Failed to start the Flask app: {str(e)}")