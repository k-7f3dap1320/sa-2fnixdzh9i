""" Tradingview watchlist """


def get_tradingview_watchlist(width,height):
    ret = ''

    tradingview = '' +\

<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-market-quotes.js" async>
  {
  "width": "100%",
  "height": "100%",
  "symbolsGroups": [
    {
      "name": "List",
      "symbols": [
        {
          "name": "OANDA:SPX500USD",
          "displayName": "S&P 500"
        },
        {
          "name": "OANDA:NAS100USD",
          "displayName": "Nasdaq 100"
        },
        {
          "name": "FOREXCOM:DJI",
          "displayName": "Dow 30"
        },
        {
          "name": "INDEX:NKY",
          "displayName": "Nikkei 225"
        },
        {
          "name": "INDEX:DEU30",
          "displayName": "DAX Index"
        },
        {
          "name": "OANDA:UK100GBP",
          "displayName": "FTSE 100"
        }
      ]
    },
    {
      "name": "List 2",
      "symbols": [
        {
          "name": "OANDA:SPX500USD",
          "displayName": "S&P 500"
        },
        {
          "name": "OANDA:NAS100USD",
          "displayName": "Nasdaq 100"
        },
        {
          "name": "FOREXCOM:DJI",
          "displayName": "Dow 30"
        },
        {
          "name": "INDEX:NKY",
          "displayName": "Nikkei 225"
        },
        {
          "name": "INDEX:DEU30",
          "displayName": "DAX Index"
        },
        {
          "name": "OANDA:UK100GBP",
          "displayName": "FTSE 100"
        }
      ]
    }
  ],
  "locale": "en",
  "largeChartUrl": "http://xx"
}
  </script>
</div>



    return ret
