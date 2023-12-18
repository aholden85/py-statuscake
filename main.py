import requests

class StatusCakeSession(requests.Session):
    """The session handles authentication and allows for request persistence.
    """

    def init_basic_auth(self, api_key: str) -> None:
        """Attach the Authorization header to the session in the correct format.
        
        As StatusCake authentication only requires an API key, which should be
        known by the operator, we only require the population of the
        Authorization header.
        
        Args:
            api_key (str): The API key to use in all StatusCake requests.
        """
        self.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
            }
        )


class StatusCakeClient:
    """The client abstratcts the "heavy-lifting" for constructing requests.
    """
    def __init__(self, api_key: str):
        """Initialize the client with a session, authenticate, and define the endpoint.
        """
        # Initialize the session.
        self.__session = StatusCakeSession()

        # Initialize the required authentication mechanism.
        self.__session.init_basic_auth(api_key)

        # Define the base API endpoint to make requests against.
        self.__endpoint = "https://api.statuscake.com"

    def __request(
        self,
        method: str,
        path: str,
        version: int = 1,
        params: dict = None,
        data: dict = None,
        headers: dict = None,
    ) -> requests.Response:
        """Basic function to remove this snippet of code out of every other
        function.

        Args:
            method: what type of request is being made (ie - GET, POST, DELETE).

            path: the target API URL.

            version: the API version, default is 1.

            params: any data that needs to be sent through a query string.

            data: any data that needs to be sent through the message body rather
                than through parameters in the query string. Only required for
                POST, PUT, and PATCH.

            headers: any extra headers to add to the base auth headers.

        Returns:
            requests.Response: The response from the API call.
        """
        # There are a specific set of request types that can be executed.
        valid_methods = [
            "GET",
            "OPTIONS",
            "HEAD",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
        ]
        if method not in valid_methods:
            raise ValueError(
                f"StatusCakeClient.__request: method must be one of {valid_methods}.",
            )

        if headers is None:
            headers = {}

        req = requests.Request(
            method=method,
            url=f"{self.__endpoint}/v{version}/{path}",
            params=params,
            data=data,
            headers=headers,
        )

        # If any data is being passed, it will need to have the Content-Type header set.
        if data is not None:
            req.headers["Content-Type"] = "application/json"

        # Execute the request, and return the JSON payload.
        prep = self.__session.prepare_request(req)
        resp = self.__session.send(prep).json()

        if 'metadata' in resp:
            print("'metadata' key present")
            return_data = []
            load_complete = False
            while not load_complete:
                return_data = return_data + resp['data']

                if resp['metadata']['page'] == resp['metadata']['page_count']:
                    load_complete = True
                else:
                    req.params['page'] = resp['metadata']['page'] + 1
                    prep = self.__session.prepare_request(req)
                    resp = self.__session.send(prep).json()
            resp['data'] = return_data
            del resp['metadata']

        return resp

    def get_all_pagespeed_checks(self) -> requests.Response:
        """Returns a list of pagespeed checks for an account.

        https://developers.statuscake.com/api/#tag/pagespeed/operation/list-pagespeed-tests
        """
        return self.__request(
            method="GET",
            path="pagespeed",
        )

    def get_all_uptime_checks(self) -> requests.Response:
        """Returns a list of uptime checks for an account.

        https://developers.statuscake.com/api/#tag/uptime/operation/list-uptime-tests
        """
        return self.__request(
            method="GET",
            path="uptime",
        )

    def get_all_uptime_check_periods(self, test_id) -> requests.Response:
        """Returns a list of uptime check periods for a given id, detailing the
        creation time of the period, when it ended and the duration.

        The returned results are a paginated series. Alongside the response data
        is a links object referencing the current response document, self.
        
        https://developers.statuscake.com/api/#tag/uptime/operation/list-uptime-test-periods
        """
        return self.__request(
            method="GET",
            path=f"uptime/{test_id}/periods",
        )
