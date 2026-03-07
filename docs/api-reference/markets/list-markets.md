# List markets



## OpenAPI

````yaml api-reference/gamma-openapi.json get /markets
openapi: 3.0.3
info:
  title: Markets API
  version: 1.0.0
  description: REST API specification for public endpoints used by the Markets service.
servers:
  - url: https://gamma-api.polymarket.com
    description: Polymarket Gamma API Production Server
security: []
tags:
  - name: Health
    description: Health check endpoints
  - name: Sports
    description: Sports-related endpoints including teams and game data
  - name: Tags
    description: Tag management and related tag operations
  - name: Events
    description: Event management and event-related operations
  - name: Markets
    description: Market data and market-related operations
  - name: Comments
    description: Comment system and user interactions
  - name: Series
    description: Series management and related operations
  - name: Profiles
    description: User profile management
  - name: Search
    description: Search functionality across different entity types
paths:
  /markets:
    get:
      tags:
        - Markets
      summary: List markets
      operationId: listMarkets
      parameters:
        - $ref: '#/components/parameters/limit'
        - $ref: '#/components/parameters/offset'
        - $ref: '#/components/parameters/order'
        - $ref: '#/components/parameters/ascending'
        - name: id
          in: query
          schema:
            type: array
            items:
              type: integer
        - name: slug
          in: query
          schema:
            type: array
            items:
              type: string
        - name: clob_token_ids
          in: query
          schema:
            type: array
            items:
              type: string
        - name: condition_ids
          in: query
          schema:
            type: array
            items:
              type: string
        - name: market_maker_address
          in: query
          schema:
            type: array
            items:
              type: string
        - name: liquidity_num_min
          in: query
          schema:
            type: number
        - name: liquidity_num_max
          in: query
          schema:
            type: number
        - name: volume_num_min
          in: query
          schema:
            type: number
        - name: volume_num_max
          in: query
          schema:
            type: number
        - name: start_date_min
          in: query
          schema:
            type: string
            format: date-time
        - name: start_date_max
          in: query
          schema:
            type: string
            format: date-time
        - name: end_date_min
          in: query
          schema:
            type: string
            format: date-time
        - name: end_date_max
          in: query
          schema:
            type: string
            format: date-time
        - name: tag_id
          in: query
          schema:
            type: integer
        - name: related_tags
          in: query
          schema:
            type: boolean
        - name: cyom
          in: query
          schema:
            type: boolean
        - name: uma_resolution_status
          in: query
          schema:
            type: string
        - name: game_id
          in: query
          schema:
            type: string
        - name: sports_market_types
          in: query
          schema:
            type: array
            items:
              type: string
        - name: rewards_min_size
          in: query
          schema:
            type: number
        - name: question_ids
          in: query
          schema:
            type: array
            items:
              type: string
        - name: include_tag
          in: query
          schema:
            type: boolean
        - name: closed
          in: query
          schema:
            type: boolean
      responses:
        '200':
          description: List of markets
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Market'
components:
  parameters:
    limit:
      name: limit
      in: query
      schema:
        type: integer
        minimum: 0
    offset:
      name: offset
      in: query
      schema:
        type: integer
        minimum: 0
    order:
      name: order
      in: query
      schema:
        type: string
      description: Comma-separated list of fields to order by
    ascending:
      name: ascending
      in: query
      schema:
        type: boolean
  schemas:
    Market:
      type: object
      properties:
        id:
          type: string
        question:
          type: string
          nullable: true
        conditionId:
          type: string
        slug:
          type: string
          nullable: true
        twitterCardImage:
          type: string
          nullable: true
        resolutionSource:
          type: string
          nullable: true
        endDate:
          type: string
          format: date-time
          nullable: true
        category:
          type: string
          nullable: true
        ammType:
          type: string
          nullable: true
        liquidity:
          type: string
          nullable: true
        sponsorName:
          type: string
          nullable: true
        sponsorImage:
          type: string
          nullable: true
        startDate:
          type: string
          format: date-time
          nullable: true
        xAxisValue:
          type: string
          nullable: true
        yAxisValue:
          type: string
          nullable: true
        denominationToken:
          type: string
          nullable: true
        fee:
          type: string
          nullable: true
        image:
          type: string
          nullable: true
        icon:
          type: string
          nullable: true
        lowerBound:
          type: string
          nullable: true
        upperBound:
          type: string
          nullable: true
        description:
          type: string
          nullable: true
        outcomes:
          type: string
          nullable: true
        outcomePrices:
          type: string
          nullable: true
        volume:
          type: string
          nullable: true
        active:
          type: boolean
          nullable: true
        marketType:
          type: string
          nullable: true
        formatType:
          type: string
          nullable: true
        lowerBoundDate:
          type: string
          nullable: true
        upperBoundDate:
          type: string
          nullable: true
        closed:
          type: boolean
          nullable: true
        marketMakerAddress:
          type: string
        createdBy:
          type: integer
          nullable: true
        updatedBy:
          type: integer
          nullable: true
        createdAt:
          type: string
          format: date-time
          nullable: true
        updatedAt:
          type: string
          format: date-time
          nullable: true
        closedTime:
          type: string
          nullable: true
        wideFormat:
          type: boolean
          nullable: true
        new:
          type: boolean
          nullable: true
        mailchimpTag:
          type: string
          nullable: true
        featured:
          type: boolean
          nullable: true
        archived:
          type: boolean
          nullable: true
        resolvedBy:
          type: string
          nullable: true
        restricted:
          type: boolean
          nullable: true
        marketGroup:
          type: integer
          nullable: true
        groupItemTitle:
          type: string
          nullable: true
        groupItemThreshold:
          type: string
          nullable: true
        questionID:
          type: string
          nullable: true
        umaEndDate:
          type: string
          nullable: true
        enableOrderBook:
          type: boolean
          nullable: true
        orderPriceMinTickSize:
          type: number
          nullable: true
        orderMinSize:
          type: number
          nullable: true
        umaResolutionStatus:
          type: string
          nullable: true
        curationOrder:
          type: integer
          nullable: true
        volumeNum:
          type: number
          nullable: true
        liquidityNum:
          type: number
          nullable: true
        endDateIso:
          type: string
          nullable: true
        startDateIso:
          type: string
          nullable: true
        umaEndDateIso:
          type: string
          nullable: true
        hasReviewedDates:
          type: boolean
          nullable: true
        readyForCron:
          type: boolean
          nullable: true
        commentsEnabled:
          type: boolean
          nullable: true
        volume24hr:
          type: number
          nullable: true
        volume1wk:
          type: number
          nullable: true
        volume1mo:
          type: number
          nullable: true
        volume1yr:
          type: number
          nullable: true
        gameStartTime:
          type: string
          nullable: true
        secondsDelay:
          type: integer
          nullable: true
        clobTokenIds:
          type: string
          nullable: true
        disqusThread:
          type: string
          nullable: true
        shortOutcomes:
          type: string
          nullable: true
        teamAID:
          type: string
          nullable: true
        teamBID:
          type: string
          nullable: true
        umaBond:
          type: string
          nullable: true
        umaReward:
          type: string
          nullable: true
        fpmmLive:
          type: boolean
          nullable: true
        volume24hrAmm:
          type: number
          nullable: true
        volume1wkAmm:
          type: number
          nullable: true
        volume1moAmm:
          type: number
          nullable: true
        volume1yrAmm:
          type: number
          nullable: true
        volume24hrClob:
          type: number
          nullable: true
        volume1wkClob:
          type: number
          nullable: true
        volume1moClob:
          type: number
          nullable: true
        volume1yrClob:
          type: number
          nullable: true
        volumeAmm:
          type: number
          nullable: true
        volumeClob:
          type: number
          nullable: true
        liquidityAmm:
          type: number
          nullable: true
        liquidityClob:
          type: number
          nullable: true
        makerBaseFee:
          type: integer
          nullable: true
        takerBaseFee:
          type: integer
          nullable: true
        customLiveness:
          type: integer
          nullable: true
        acceptingOrders:
          type: boolean
          nullable: true
        notificationsEnabled:
          type: boolean
          nullable: true
        score:
          type: integer
          nullable: true
        imageOptimized:
          $ref: '#/components/schemas/ImageOptimization'
        iconOptimized:
          $ref: '#/components/schemas/ImageOptimization'
        events:
          type: array
          items:
            $ref: '#/components/schemas/Event'
        categories:
          type: array
          items:
            $ref: '#/components/schemas/Category'
        tags:
          type: array
          items:
            $ref: '#/components/schemas/Tag'
        creator:
          type: string
          nullable: true
        ready:
          type: boolean
          nullable: true
        funded:
          type: boolean
          nullable: true
        pastSlugs:
          type: string
          nullable: true
        readyTimestamp:
          type: string
          format: date-time
          nullable: true
        fundedTimestamp:
          type: string
          format: date-time
          nullable: true
        acceptingOrdersTimestamp:
          type: string
          format: date-time
          nullable: true
        competitive:
          type: number
          nullable: true
        rewardsMinSize:
          type: number
          nullable: true
        rewardsMaxSpread:
          type: number
          nullable: true
        spread:
          type: number
          nullable: true
        automaticallyResolved:
          type: boolean
          nullable: true
        oneDayPriceChange:
          type: number
          nullable: true
        oneHourPriceChange:
          type: number
          nullable: true
        oneWeekPriceChange:
          type: number
          nullable: true
        oneMonthPriceChange:
          type: number
          nullable: true
        oneYearPriceChange:
          type: number
          nullable: true
        lastTradePrice:
          type: number
          nullable: true
        bestBid:
          type: number
          nullable: true
        bestAsk:
          type: number
          nullable: true
        automaticallyActive:
          type: boolean
          nullable: true
        clearBookOnStart:
          type: boolean
          nullable: true
        chartColor:
          type: string
          nullable: true
        seriesColor:
          type: string
          nullable: true
        showGmpSeries:
          type: boolean
          nullable: true
        showGmpOutcome:
          type: boolean
          nullable: true
        manualActivation:
          type: boolean
          nullable: true
        negRiskOther:
          type: boolean
          nullable: true
        gameId:
          type: string
          nullable: true
        groupItemRange:
          type: string
          nullable: true
        sportsMarketType:
          type: string
          nullable: true
        line:
          type: number
          nullable: true
        umaResolutionStatuses:
          type: string
          nullable: true
        pendingDeployment:
          type: boolean
          nullable: true
        deploying:
          type: boolean
          nullable: true
        deployingTimestamp:
          type: string
          format: date-time
          nullable: true
        scheduledDeploymentTimestamp:
          type: string
          format: date-time
          nullable: true
        rfqEnabled:
          type: boolean
          nullable: true
        eventStartTime:
          type: string
          format: date-time
          nullable: true
    ImageOptimization:
      type: object
      properties:
        id:
          type: string
        imageUrlSource:
          type: string
          nullable: true
        imageUrlOptimized:
          type: string
          nullable: true
        imageSizeKbSource:
          type: number
          nullable: true
        imageSizeKbOptimized:
          type: number
          nullable: true
        imageOptimizedComplete:
          type: boolean
          nullable: true
        imageOptimizedLastUpdated:
          type: string
          nullable: true
        relID:
          type: integer
          nullable: true
        field:
          type: string
          nullable: true
        relname:
          type: string
          nullable: true
    Event:
      type: object
      properties:
        id:
          type: string
        ticker:
          type: string
          nullable: true
        slug:
          type: string
          nullable: true
        title:
          type: string
          nullable: true
        subtitle:
          type: string
          nullable: true
        description:
          type: string
          nullable: true
        resolutionSource:
          type: string
          nullable: true
        startDate:
          type: string
          format: date-time
          nullable: true
        creationDate:
          type: string
          format: date-time
          nullable: true
        endDate:
          type: string
          format: date-time
          nullable: true
        image:
          type: string
          nullable: true
        icon:
          type: string
          nullable: true
        active:
          type: boolean
          nullable: true
        closed:
          type: boolean
          nullable: true
        archived:
          type: boolean
          nullable: true
        new:
          type: boolean
          nullable: true
        featured:
          type: boolean
          nullable: true
        restricted:
          type: boolean
          nullable: true
        liquidity:
          type: number
          nullable: true
        volume:
          type: number
          nullable: true
        openInterest:
          type: number
          nullable: true
        sortBy:
          type: string
          nullable: true
        category:
          type: string
          nullable: true
        subcategory:
          type: string
          nullable: true
        isTemplate:
          type: boolean
          nullable: true
        templateVariables:
          type: string
          nullable: true
        published_at:
          type: string
          nullable: true
        createdBy:
          type: string
          nullable: true
        updatedBy:
          type: string
          nullable: true
        createdAt:
          type: string
          format: date-time
          nullable: true
        updatedAt:
          type: string
          format: date-time
          nullable: true
        commentsEnabled:
          type: boolean
          nullable: true
        competitive:
          type: number
          nullable: true
        volume24hr:
          type: number
          nullable: true
        volume1wk:
          type: number
          nullable: true
        volume1mo:
          type: number
          nullable: true
        volume1yr:
          type: number
          nullable: true
        featuredImage:
          type: string
          nullable: true
        disqusThread:
          type: string
          nullable: true
        parentEvent:
          type: string
          nullable: true
        enableOrderBook:
          type: boolean
          nullable: true
        liquidityAmm:
          type: number
          nullable: true
        liquidityClob:
          type: number
          nullable: true
        negRisk:
          type: boolean
          nullable: true
        negRiskMarketID:
          type: string
          nullable: true
        negRiskFeeBips:
          type: integer
          nullable: true
        commentCount:
          type: integer
          nullable: true
        imageOptimized:
          $ref: '#/components/schemas/ImageOptimization'
        iconOptimized:
          $ref: '#/components/schemas/ImageOptimization'
        featuredImageOptimized:
          $ref: '#/components/schemas/ImageOptimization'
        subEvents:
          type: array
          items:
            type: string
          nullable: true
        markets:
          type: array
          items:
            $ref: '#/components/schemas/Market'
        series:
          type: array
          items:
            $ref: '#/components/schemas/Series'
        categories:
          type: array
          items:
            $ref: '#/components/schemas/Category'
        collections:
          type: array
          items:
            $ref: '#/components/schemas/Collection'
        tags:
          type: array
          items:
            $ref: '#/components/schemas/Tag'
        cyom:
          type: boolean
          nullable: true
        closedTime:
          type: string
          format: date-time
          nullable: true
        showAllOutcomes:
          type: boolean
          nullable: true
        showMarketImages:
          type: boolean
          nullable: true
        automaticallyResolved:
          type: boolean
          nullable: true
        enableNegRisk:
          type: boolean
          nullable: true
        automaticallyActive:
          type: boolean
          nullable: true
        eventDate:
          type: string
          nullable: true
        startTime:
          type: string
          format: date-time
          nullable: true
        eventWeek:
          type: integer
          nullable: true
        seriesSlug:
          type: string
          nullable: true
        score:
          type: string
          nullable: true
        elapsed:
          type: string
          nullable: true
        period:
          type: string
          nullable: true
        live:
          type: boolean
          nullable: true
        ended:
          type: boolean
          nullable: true
        finishedTimestamp:
          type: string
          format: date-time
          nullable: true
        gmpChartMode:
          type: string
          nullable: true
        eventCreators:
          type: array
          items:
            $ref: '#/components/schemas/EventCreator'
        tweetCount:
          type: integer
          nullable: true
        chats:
          type: array
          items:
            $ref: '#/components/schemas/Chat'
        featuredOrder:
          type: integer
          nullable: true
        estimateValue:
          type: boolean
          nullable: true
        cantEstimate:
          type: boolean
          nullable: true
        estimatedValue:
          type: string
          nullable: true
        templates:
          type: array
          items:
            $ref: '#/components/schemas/Template'
        spreadsMainLine:
          type: number
          nullable: true
        totalsMainLine:
          type: number
          nullable: true
        carouselMap:
          type: string
          nullable: true
        pendingDeployment:
          type: boolean
          nullable: true
        deploying:
          type: boolean
          nullable: true
        deployingTimestamp:
          type: string
          format: date-time
          nullable: true
        scheduledDeploymentTimestamp:
          type: string
          format: date-time
          nullable: true
        gameStatus:
          type: string
          nullable: true
    Category:
      type: object
      properties:
        id:
          type: string
        label:
          type: string
          nullable: true
        parentCategory:
          type: string
          nullable: true
        slug:
          type: string
          nullable: true
        publishedAt:
          type: string
          nullable: true
        createdBy:
          type: string
          nullable: true
        updatedBy:
          type: string
          nullable: true
        createdAt:
          type: string
          format: date-time
          nullable: true
        updatedAt:
          type: string
          format: date-time
          nullable: true
    Tag:
      type: object
      properties:
        id:
          type: string
        label:
          type: string
          nullable: true
        slug:
          type: string
          nullable: true
        forceShow:
          type: boolean
          nullable: true
        publishedAt:
          type: string
          nullable: true
        createdBy:
          type: integer
          nullable: true
        updatedBy:
          type: integer
          nullable: true
        createdAt:
          type: string
          format: date-time
          nullable: true
        updatedAt:
          type: string
          format: date-time
          nullable: true
        forceHide:
          type: boolean
          nullable: true
        isCarousel:
          type: boolean
          nullable: true
    Series:
      type: object
      properties:
        id:
          type: string
        ticker:
          type: string
          nullable: true
        slug:
          type: string
          nullable: true
        title:
          type: string
          nullable: true
        subtitle:
          type: string
          nullable: true
        seriesType:
          type: string
          nullable: true
        recurrence:
          type: string
          nullable: true
        description:
          type: string
          nullable: true
        image:
          type: string
          nullable: true
        icon:
          type: string
          nullable: true
        layout:
          type: string
          nullable: true
        active:
          type: boolean
          nullable: true
        closed:
          type: boolean
          nullable: true
        archived:
          type: boolean
          nullable: true
        new:
          type: boolean
          nullable: true
        featured:
          type: boolean
          nullable: true
        restricted:
          type: boolean
          nullable: true
        isTemplate:
          type: boolean
          nullable: true
        templateVariables:
          type: boolean
          nullable: true
        publishedAt:
          type: string
          nullable: true
        createdBy:
          type: string
          nullable: true
        updatedBy:
          type: string
          nullable: true
        createdAt:
          type: string
          format: date-time
          nullable: true
        updatedAt:
          type: string
          format: date-time
          nullable: true
        commentsEnabled:
          type: boolean
          nullable: true
        competitive:
          type: string
          nullable: true
        volume24hr:
          type: number
          nullable: true
        volume:
          type: number
          nullable: true
        liquidity:
          type: number
          nullable: true
        startDate:
          type: string
          format: date-time
          nullable: true
        pythTokenID:
          type: string
          nullable: true
        cgAssetName:
          type: string
          nullable: true
        score:
          type: integer
          nullable: true
        events:
          type: array
          items:
            $ref: '#/components/schemas/Event'
        collections:
          type: array
          items:
            $ref: '#/components/schemas/Collection'
        categories:
          type: array
          items:
            $ref: '#/components/schemas/Category'
        tags:
          type: array
          items:
            $ref: '#/components/schemas/Tag'
        commentCount:
          type: integer
          nullable: true
        chats:
          type: array
          items:
            $ref: '#/components/schemas/Chat'
    Collection:
      type: object
      properties:
        id:
          type: string
        ticker:
          type: string
          nullable: true
        slug:
          type: string
          nullable: true
        title:
          type: string
          nullable: true
        subtitle:
          type: string
          nullable: true
        collectionType:
          type: string
          nullable: true
        description:
          type: string
          nullable: true
        tags:
          type: string
          nullable: true
        image:
          type: string
          nullable: true
        icon:
          type: string
          nullable: true
        headerImage:
          type: string
          nullable: true
        layout:
          type: string
          nullable: true
        active:
          type: boolean
          nullable: true
        closed:
          type: boolean
          nullable: true
        archived:
          type: boolean
          nullable: true
        new:
          type: boolean
          nullable: true
        featured:
          type: boolean
          nullable: true
        restricted:
          type: boolean
          nullable: true
        isTemplate:
          type: boolean
          nullable: true
        templateVariables:
          type: string
          nullable: true
        publishedAt:
          type: string
          nullable: true
        createdBy:
          type: string
          nullable: true
        updatedBy:
          type: string
          nullable: true
        createdAt:
          type: string
          format: date-time
          nullable: true
        updatedAt:
          type: string
          format: date-time
          nullable: true
        commentsEnabled:
          type: boolean
          nullable: true
        imageOptimized:
          $ref: '#/components/schemas/ImageOptimization'
        iconOptimized:
          $ref: '#/components/schemas/ImageOptimization'
        headerImageOptimized:
          $ref: '#/components/schemas/ImageOptimization'
    EventCreator:
      type: object
      properties:
        id:
          type: string
        creatorName:
          type: string
          nullable: true
        creatorHandle:
          type: string
          nullable: true
        creatorUrl:
          type: string
          nullable: true
        creatorImage:
          type: string
          nullable: true
        createdAt:
          type: string
          format: date-time
          nullable: true
        updatedAt:
          type: string
          format: date-time
          nullable: true
    Chat:
      type: object
      properties:
        id:
          type: string
        channelId:
          type: string
          nullable: true
        channelName:
          type: string
          nullable: true
        channelImage:
          type: string
          nullable: true
        live:
          type: boolean
          nullable: true
        startTime:
          type: string
          format: date-time
          nullable: true
        endTime:
          type: string
          format: date-time
          nullable: true
    Template:
      type: object
      properties:
        id:
          type: string
        eventTitle:
          type: string
          nullable: true
        eventSlug:
          type: string
          nullable: true
        eventImage:
          type: string
          nullable: true
        marketTitle:
          type: string
          nullable: true
        description:
          type: string
          nullable: true
        resolutionSource:
          type: string
          nullable: true
        negRisk:
          type: boolean
          nullable: true
        sortBy:
          type: string
          nullable: true
        showMarketImages:
          type: boolean
          nullable: true
        seriesSlug:
          type: string
          nullable: true
        outcomes:
          type: string
          nullable: true

````

---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt