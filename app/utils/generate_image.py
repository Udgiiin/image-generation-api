from app.core.config import settings
import requests

class ApiImage:

    def execute(self, path):
        return requests.get(url=settings.IMAGEAPI + path)

    def generate(self, slug):
        return self.execute(f"/monster/{slug}")

api_image = ApiImage()