# python_scrape_attempt
This was my attempt for scraping URLs with playwright built in a lambda, posting for review to have someone else make it work.  
  
testlambda.py contains the actual function executed by the lambda, it works great dockerized locally, but I was not able to get it to function once that container is uploaded to ECR and used by an AWS Lambda Function. It passed all stealth tests, the _only_ minor downside compared to node/puppeteer is no adblock/block-resources was available that I could find - but that is not a dealbreaker.
  
Since I never got this to work as a lambda, I'll admit I got closer/spent more time trying with node/puppeteer - That project is here -> https://github.com/pubtxmadison/node_scrape_attempt


### I would honestly MUCH PREFER this be the solution, I am more comfortable with python.  
  
But I'll take what I can get.
