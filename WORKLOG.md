## Work Log
Document meant to keep track of my thoughts while developing this app

___



### First read

First read of the assignment, my approach is to look for a MVP going straight for the assignment requirements, then I will have to judge which improvements can be done along the way without slowing me down too much while keeping the rest for later.

I know I will work with Python and even if I have everything setup on my local machine I want whoever to be able to run it easily so let's Dockerize it! I want to work with CSV data so I'll look for an efficient way to validate the data and make it ready to process.

The given samples might be quite light but I want to be mindful of the use-cases for the app I'm building, including larger datasets to process in the future.

I will go ahead and use `black` as python formatter from habits and setup, shouldn't matter



### Development

Picked `pandas` to work with dataframes, worked with it before for simple operations, that should make my life easy with all the methods baked in. Also gives me some sense of scaling with the option to import files as chunks if they would get larger. Of course it exists many other packages and built on top of `pandas` API with crazy import optimisation, clustering options etc but that would just be over-engineering at the MVP stage.

Got the desired output file, input validation was made through `pandas` methods to check for duplicates but also the way I grab the data from unique entries it will only work with non-null values and no duplicate to be able to match.

Breaking down my script into methods to have some modularity, code easy to read or re-use/adapt. Additionally I will work with typing in my methods syntax, mainly because of habits but also not a `pandas` expert so I like to keep track of the expected types I work with and return values from my methods.

Now it's executing fast which is expected with the samples size and my machine, with my bit of refactoring the script is ready to receive upgrades for file import if necessary in the future.

#### Testing

Code is written as the given samples are the only CSV files we would get or exact same templates with different values. With the import we are doing, we get rid of all basic input errors such as wrong format, empty files etc
Regarding test coverage, always good to aim for complete test coverage to make sure everything does what it is supposed to and also for future additions some regression tests to make sure nothing changed.

Could have done some TDD, but the development method was more trial and error, working with dataframes is similar to adjusting SELECT queries for a SQL database, we grab the data we want and format it as we go. Had the format but not the proper end result which I was building along the way so that was more convenient.

Here by lack of time and relevance, I'll add unit tests thoughts to improvements



#### Bonuses

Simply creating one method for each bonus section to make it clearer for me, then I can just call these methods wherever and whenever I want.
Done with the coding bonuses, was pretty fast once again thanks to `pandas` between the documentation and the big community around it.

Will tackle the Database model now which makes me happy cause with what I have built the obvious comes to my mind: If you are planning on working with your data set over time, its probably best to get the data into a database of some type.

Right now it is CSV files, one defined execution with one defined result but realistically a product related to this data should grow constantly with new customers making new orders getting new barcodes.

Anyway, jumping in MIRO, I do a mix of Draw.io also but here clean and fast for a simple diagram, will just go with MIRO quick wins.

Alright so for the modelling of our SQL database, same as the code we want to project today's requirements while standing ready for more, will create one entity for each with relations according to today's given rules. Will take the liberty of creating an extra for Customers today holding only IDs but maybe we want to extend that with extra customer related data to gather for analytics or other use.
Indexes? Yes would be nice since we can already imagine the queries we would make based on our work with dataframes we are not gonna sleep on free optimisation!

We know we will need to query by grouping Orders/Barcodes (JOIN etc) on the `order_id` so it will be our index for now.

#### Diagram

![ntity Relationship Diagra](/Users/guiz/Downloads/Entity Relationship Diagram.jpg)



### Improvements

**Note**: I have a solid interest into software products, how they could be viable in the outside world with real life use cases, with that said I cannot help thinking about how this app would really look like outside of this very specific isolated case

I've been playing around the data, requesting different things to try it out, changing bits of the input files along with imagining how this app would be viable for a real product scenarios living in the cloud so here are my key take aways:

- Tests coverage, deeper validation if we would know let's say the `barcodes` format at all times for down to the value validation
- If we really want to work with files, instead of being static it could live in AWS s3 bucket temporary, upload from whichever source as CSV, then with event based we could fetch files and process them to create the vouchers
- Now once again in the outside world this data will grow and should live in a database, then either it is populated from somewhere else and we just query what we want following our model or it could be populated by the same service if we judge we want this part to live under the same roof, in this case converting it to an API? Where we can POST and populate our entities and later on GET vouchers either from a query creating what we want or an optional extra Vouchers entity keeping track of all created Vouchers?
- For things such as top customers, we don't want to run the same query 100 times, so we could cache the top using Redis or any other key/value cause the database will reach a point where the best customers will not change each second etc
