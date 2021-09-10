# Problem 1

The `order_records.log` file consists of json logs for each order. Each log has the order's weight and volume, as well as an indication if the package information is either in imperial units (pounds and inches cubed) or not (kilograms and centimeters cubed), the delivery and pickup zip codes, the expense, the company id, the driver type, and the service_line.

For this exercise, we want you to read in the data, clean it, transform it into the formats outlined below, and save the processed data. The methods you use are up to you but, at a minimum, your solution should satify the following items:

1. Your work should include an executable python file named `main.py` which runs your entire solution to this exercise.
2. Your `main.py` must have the `boolean` input `imperial_units` which defines the units in which the processed data must be saved.
3. The output data should be a pandas dataframe and `main.py` must save the dataframe as the pickle object `output.p`.
4. `output.p` must only have the following columns and associated types:
    * `order_id`: `int`
    * `company_id`: `int`
    * `service_line`: `int`
    * `driver_type`: `str`
    * `expense`: `float`
    * `weight`: `float`
    * `volume`: `float`

5. Inside the `problem_1` directory, we will run `python3 main.py` or `python3 main.py -imperial_units <boolean>` to execute and evaluate your work. If `-imperial_units` is not specified, default to `imperial_units=True`.
6. (Bonus - optional) Could you identify something in the data that is not physically possible? Please submit your answer as `bonus.txt`.

Good luck!
