# How to Fetch Markets

<Tip>Both the getEvents and getMarkets are paginated. See [pagination section](#pagination) for details.</Tip>
This guide covers the three recommended approaches for fetching market data from the Gamma API, each optimized for different use cases.

## Overview

There are three main strategies for retrieving market data:

1. **By Slug** - Best for fetching specific individual markets or events
2. **By Tags** - Ideal for filtering markets by category or sport
3. **Via Events Endpoint** - Most efficient for retrieving all active markets

***

## 1. Fetch by Slug

**Use Case:** When you need to retrieve a specific market or event that you already know about.

Individual markets and events are best fetched using their unique slug identifier. The slug can be found directly in the Polymarket frontend URL.

### How to Extract the Slug

From any Polymarket URL, the slug is the path segment after `/event/` or `/market/`:

```
https://polymarket.com/event/fed-decision-in-october?tid=1758818660485
                            ↑
                  Slug: fed-decision-in-october
```

### API Endpoints

**For Events:** [GET /events/slug/{slug}](/api-reference/events/list-events)

**For Markets:** [GET /markets/slug/{slug}](/api-reference/markets/list-markets)

### Examples

```bash  theme={null}
curl "https://gamma-api.polymarket.com/events/slug/fed-decision-in-october"
```

***

## 2. Fetch by Tags

**Use Case:** When you want to filter markets by category, sport, or topic.

Tags provide a powerful way to categorize and filter markets. You can discover available tags and then use them to filter your market requests.

### Discover Available Tags

**General Tags:** [GET /tags](/api-reference/tags/list-tags)

**Sports Tags & Metadata:** [GET /sports](/api-reference/sports/get-sports-metadata-information)

The `/sports` endpoint returns comprehensive metadata for sports including tag IDs, images, resolution sources, and series information.

### Using Tags in Market Requests

Once you have tag IDs, you can use them with the `tag_id` parameter in both markets and events endpoints.

**Markets with Tags:** [GET /markets](/api-reference/markets/list-markets)

**Events with Tags:** [GET /events](/api-reference/events/list-events)

```bash  theme={null}
curl "https://gamma-api.polymarket.com/events?tag_id=100381&limit=1&closed=false"

```

### Additional Tag Filtering

You can also:

* Use `related_tags=true` to include related tag markets
* Exclude specific tags with `exclude_tag_id`

***

## 3. Fetch All Active Markets

**Use Case:** When you need to retrieve all available active markets, typically for broader analysis or market discovery.

The most efficient approach is to use the `/events` endpoint and work backwards, as events contain their associated markets.

**Events Endpoint:** [GET /events](/api-reference/events/list-events)

**Markets Endpoint:** [GET /markets](/api-reference/markets/list-markets)

### Key Parameters

* `order=id` - Order by event ID
* `ascending=false` - Get newest events first
* `closed=false` - Only active markets
* `limit` - Control response size
* `offset` - For pagination

### Examples

```bash  theme={null}
curl "https://gamma-api.polymarket.com/events?order=id&ascending=false&closed=false&limit=100"
```

This approach gives you all active markets ordered from newest to oldest, allowing you to systematically process all available trading opportunities.

### Pagination

For large datasets, use pagination with `limit` and `offset` parameters:

* `limit=50` - Return 50 results per page
* `offset=0` - Start from the beginning (increment by limit for subsequent pages)

**Pagination Examples:**

```bash  theme={null}
# Page 1: First 50 results (offset=0)
curl "https://gamma-api.polymarket.com/events?order=id&ascending=false&closed=false&limit=50&offset=0"
```

```bash  theme={null}
# Page 2: Next 50 results (offset=50)
curl "https://gamma-api.polymarket.com/events?order=id&ascending=false&closed=false&limit=50&offset=50"
```

```bash  theme={null}
# Page 3: Next 50 results (offset=100)
curl "https://gamma-api.polymarket.com/events?order=id&ascending=false&closed=false&limit=50&offset=100"
```

```bash  theme={null}
# Paginating through markets with tag filtering
curl "https://gamma-api.polymarket.com/markets?tag_id=100381&closed=false&limit=25&offset=0"
```

```bash  theme={null}
# Next page of markets with tag filtering
curl "https://gamma-api.polymarket.com/markets?tag_id=100381&closed=false&limit=25&offset=25"
```

***

## Best Practices

1. **For Individual Markets:** Always use the slug method for best performance
2. **For Category Browsing:** Use tag filtering to reduce API calls
3. **For Complete Market Discovery:** Use the events endpoint with pagination
4. **Always Include `closed=false`:** Unless you specifically need historical data
5. **Implement Rate Limiting:** Respect API limits for production applications

## Related Endpoints

* [Get Markets](/developers/gamma-markets-api/get-markets) - Full markets endpoint documentation
* [Get Events](/developers/gamma-markets-api/get-events) - Full events endpoint documentation
* [Search Markets](/developers/gamma-markets-api/get-public-search) - Search functionality


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt