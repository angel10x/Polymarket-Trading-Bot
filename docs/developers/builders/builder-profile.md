# Builder Profile & Keys

> Learn how to access your builder profile and obtain API credentials

## Accessing Your Builder Profile

<CardGroup cols={2}>
  <Card title="Direct Link" icon="link">
    Go to [polymarket.com/settings?tab=builder](https://polymarket.com/settings?tab=builder)
  </Card>

  <Card title="From Profile Menu" icon="user">
    Click your profile image and Select "Builders"
  </Card>
</CardGroup>

***

## Builder Profile Settings

<img src="https://mintcdn.com/polymarket-292d1b1b/Quu9lXyXHL-5rjVX/images/builder-profile-image.png?fit=max&auto=format&n=Quu9lXyXHL-5rjVX&q=85&s=67176050b411016e3bfea47bc6fd8fbb" alt="Builder Settings Page" data-og-width="1854" width="1854" data-og-height="1056" height="1056" data-path="images/builder-profile-image.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/polymarket-292d1b1b/Quu9lXyXHL-5rjVX/images/builder-profile-image.png?w=280&fit=max&auto=format&n=Quu9lXyXHL-5rjVX&q=85&s=539b92c0a46959d583d603849459e8df 280w, https://mintcdn.com/polymarket-292d1b1b/Quu9lXyXHL-5rjVX/images/builder-profile-image.png?w=560&fit=max&auto=format&n=Quu9lXyXHL-5rjVX&q=85&s=e7141165754009d3942946b53817feb8 560w, https://mintcdn.com/polymarket-292d1b1b/Quu9lXyXHL-5rjVX/images/builder-profile-image.png?w=840&fit=max&auto=format&n=Quu9lXyXHL-5rjVX&q=85&s=1ec3abc842204033dc99acc2a1fdd9bf 840w, https://mintcdn.com/polymarket-292d1b1b/Quu9lXyXHL-5rjVX/images/builder-profile-image.png?w=1100&fit=max&auto=format&n=Quu9lXyXHL-5rjVX&q=85&s=33d5ca2e18a9267289c1075a0b6d2413 1100w, https://mintcdn.com/polymarket-292d1b1b/Quu9lXyXHL-5rjVX/images/builder-profile-image.png?w=1650&fit=max&auto=format&n=Quu9lXyXHL-5rjVX&q=85&s=5ee84537ae2c108a23f01a19581f2783 1650w, https://mintcdn.com/polymarket-292d1b1b/Quu9lXyXHL-5rjVX/images/builder-profile-image.png?w=2500&fit=max&auto=format&n=Quu9lXyXHL-5rjVX&q=85&s=ed471a4141f2e55fba0f16ad0b70aa38 2500w" />

### Customize Your Builder Identity

* **Profile Picture**: Upload a custom image for the [Builder Leaderboard](https://builders.polymarket.com/)
* **Builder Name**: Set the name displayed publicly on the leaderboard

### View Your Builder Information

* **Builder Address**: Your unique builder address for identification
* **Creation Date**: When your builder account was created
* **Current Tier**: Your rate limit tier (Unverified or Verified)

***

## Builder API Keys

Builder API keys are required to access the relayer and for CLOB order attribution.

### Creating API Keys

In the **Builder Keys** section of your profile's **Builder Settings**:

1. View existing API keys with their creation dates and status
2. Click **"+ Create New"** to generate a new API key

Each API key includes:

| Credential   | Description                          |
| ------------ | ------------------------------------ |
| `apiKey`     | Your builder API key identifier      |
| `secret`     | Secret key for signing requests      |
| `passphrase` | Additional authentication passphrase |

### Managing API Keys

* **Multiple Keys**: Create separate keys for different environments
* **Active Status**: Keys show "ACTIVE" when operational

***

## Next Steps

<CardGroup cols={2}>
  <Card title="Order Attribution" icon="tag" href="/developers/builders/order-attribution">
    Start attributing customer orders to your account
  </Card>

  <Card title="Builder Leaderboard" icon="trophy" href="https://builders.polymarket.com/">
    View your public profile and stats
  </Card>
</CardGroup>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt