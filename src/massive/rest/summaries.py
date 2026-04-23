from massive.rest.models.summaries import SummaryResult
from .base import BaseClient
from typing import Optional, Any, Dict, List, Union
from urllib3 import HTTPResponse

from .models.request import RequestOptionBuilder


class SummariesClient(BaseClient):
    def get_summaries(
        self,
        ticker_any_of: Optional[List[str]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[List[SummaryResult], HTTPResponse]:
        """
        GetSummaries retrieves summaries for the ticker list with the given params.
        For more details see https://massive.com/docs/stocks/get_v1_summaries.

        :param ticker_any_of: The ticker symbol
        :param params: Any additional query params
        :param raw: Return raw object instead of results object
        :return: SummaryResults
        """

        url = f"/v1/summaries"
        return self._get(
            path=url,
            params=self._get_params(self.get_summaries, locals()),
            result_key="results",
            deserializer=SummaryResult.from_dict,
            raw=raw,
            options=options,
        )
