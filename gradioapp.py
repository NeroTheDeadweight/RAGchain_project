# import gradio as gr
# from tgbot import save_todb, get_chat_history
# import main
# def yes_man(message, history):
#     save_todb(message)
#     answer = main.get_chunk(message)
#     save_todb(answer)
#     return answer
# demo = gr.ChatInterface(
#     yes_man,
#     chatbot=gr.Chatbot(height=300),
#     textbox=gr.Textbox(placeholder="Ask me a question", container=False, scale=7),
#     title="RAG Bot",
#     description="Ask RAGBot any question",
#     theme="soft",
#     examples=["Hello", "Am I cool?", "Are tomatoes vegetables?"],
#     cache_examples=True,
#     retry_btn=None,
#     undo_btn="Delete Previous",
#     clear_btn="Clear",
# )
# demo.launch()