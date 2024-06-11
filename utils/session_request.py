from typing import Union

class SessionRequest:
    def __init__(self, url, request_type) -> None:
        self.__url: str = url
        self.__type: str = request_type
        self.__headers: dict = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        }
        self.__response = None

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value: str):
        self.__url = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, value: dict):
        self.__headers = value

    @property
    def response(self):
        return self.__response

    @response.setter
    def response(self, value: dict):
        self.__response = value

    @property
    def response_text(self):
        return self.__response_text

    @response_text.setter
    def response_text(self, value: str):
        self.__response_text = value


    async def request(self, session, data: Union[dict, None] = None):
        """ Send request """

        if self.type == "POST":
            self.response = session.post(
                url=self.url,
                data=data,
                headers=self.headers
            )
            assert self.response.status_code == 200, "Bad request"

        elif self.type == "GET":
            self.response = session.get(
                url=self.url,
                headers=self.headers
            )
            assert self.response.status_code == 200, "Bad request"
