from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from langchain_core.messages import HumanMessage, SystemMessage
from .agent import get_shopping_assistant

class ChatBotView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_message = request.data.get('message')
        if not user_message:
            return Response({"error": "Введіть повідомлення (поле 'message')"}, status=400)

        try:
            agent = get_shopping_assistant()
            
            inputs = {
                "messages": [
                    SystemMessage(content="Ти — привітний AI-консультант магазину Shop Modivo. Допомагай шукати товари та перевіряти замовлення. Завжди відповідай українською мовою."),
                    HumanMessage(content=user_message)
                ]
            }
            
            response = agent.invoke(inputs)
            bot_reply = response["messages"][-1].content
            
            return Response({
                "user": request.user.username,
                "bot_response": bot_reply
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)