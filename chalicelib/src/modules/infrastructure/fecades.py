import os
from openai import OpenAI
import logging

LOGGER = logging.getLogger('abcall-knowledgebase-microservice')

class OpenAIService:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.openai_client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
        )

    def generate_risk_evaluation(self, flows, articles):
        # Create a concise summary of flows and articles
        flows_summary = ", ".join([flow.get("name", "N/A") for flow in flows])
        articles_summary = ", ".join([article.get("title", "N/A") for article in articles])

        # Construct the prompt for ChatGPT
        prompt = (
            f"Considera la siguiente información:\n"
            f"Flujos: {flows_summary}\n"
            f"Artículos: {articles_summary}\n"
            "Proporciona una recomendación clara y útil para un agente de servicio al cliente que pueda ayudarle "
            "a resolver eficazmente el problema del cliente. Asegúrate de que la recomendación sea práctica, "
            "específica y orientada a pasos accionables para que el agente pueda implementarla de inmediato. "
            "Asimismo, utiliza la informacion de Artículos: para ser mas preciso al proponer acciones para ayudar."
            "La recomendación debe estar en español."
        )

        try:
            # Call OpenAI API
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150
            )
            LOGGER.info("OpenAI response: %s", response)

            recommendation = response.choices[0].message.content.strip()

            return recommendation
        except Exception as e:
            LOGGER.error(f"Error calling OpenAI API: {str(e)}")
            # Return a random recommendation from a list of generic recommendations
            generic_recommendations = [
                "Asegúrate de comprender claramente el problema del cliente y ofrécele una solución paso a paso.",
                "Recomienda al cliente reiniciar su dispositivo y verificar su conexión a internet.",
                "Si el problema persiste, sugiere escalar el caso a un nivel superior para una resolución más rápida.",
                "Recuerda ser empático y asegurarte de que el cliente se sienta escuchado y comprendido.",
                "Guía al cliente a través de los pasos de solución de problemas con calma y paciencia.",
                "Proporciona detalles claros sobre las opciones disponibles y cómo el cliente puede proceder."
            ]
            return random.choice(generic_recommendations)


class MicroservicesFacade:
    def __init__(self):
        self.openai_service = OpenAIService()

    def generate_risk_evaluation(self, flows, articles):
        return self.openai_service.generate_risk_evaluation(flows, articles)


