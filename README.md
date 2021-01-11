# sugary-products-chart

# Overview

The sugary products chart is a simple chart made by interpreting the data from the [Open Food Facts](https://world.openfoodfacts.org/) Database with respect to the content of sugar of various food products.

# Run it!

## Prerequisites

Before running `process_food_facts.py` make sure to have downloaded the `CSV` file with the data from [this page](https://de.openfoodfacts.org/data) and placed it beside the `.py` script.

## Run the script

```
$ python3 process_food_facts.py
```

When the script is finished two new files will have appeared: 

* `sugary_products.csv` - contains data extracted from the Open Food Facts CSV file to be used for generating the content of `chart.js`
  
* `chart.js` - contains information, in a specific format, to be plotted by [ChartJS](https://www.chartjs.org/) (this is what the user will see in the end)

The `chart.js` is used by the `chart.html`, which by opening it in your favorite Web browser will display the visualization.

# License

This code is released under [LICENSE](LICENSE) 
