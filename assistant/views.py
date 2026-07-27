from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from .agent import get_shopping_assistant
from .models import ChatMessage


class ChatBotView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_message = request.data.get('message')
        if not user_message:
            return Response({"error": "Введіть повідомлення (поле 'message')"}, status=400)

        try:
            agent = get_shopping_assistant()

            # 1. Завантажуємо останні 10 повідомлень з БД (від старих до нових)
            history = ChatMessage.objects.filter(
                user=request.user
            ).order_by('-created_at')[:10]
            history = list(reversed(history))

            # 2. Формуємо список повідомлень для агента
            messages = [
                SystemMessage(content="Ти — привітний AI-консультант магазину Shop Modivo. Допомагай шукати товари та перевіряти замовлення. Завжди відповідай українською мовою.")
            ]

            # Додаємо минулі повідомлення з бази
            for msg in history:
                if msg.role == 'human':
                    messages.append(HumanMessage(content=msg.content))
                else:
                    messages.append(AIMessage(content=msg.content))

            # Додаємо поточне повідомлення юзера
            messages.append(HumanMessage(content=user_message))

            inputs = {"messages": messages}

            response = agent.invoke(inputs)
            bot_reply = response["messages"][-1].content

            # 3. Зберігаємо обидва повідомлення в БД
            ChatMessage.objects.create(
                user=request.user,
                role='human',
                content=user_message
            )
            ChatMessage.objects.create(
                user=request.user,
                role='ai',
                content=bot_reply
            )

            return Response({
                "user": request.user.username,
                "bot_response": bot_reply
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)