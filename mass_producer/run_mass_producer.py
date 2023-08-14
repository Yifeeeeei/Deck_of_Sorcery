from config import *

from mass_producer_xlsx import *

if __name__ == "__main__":
    config = Config_default()
    mass_producer_xlsx = MassProducerXlsx(config, "mass_producer_params_xlsx.json")
    mass_producer_xlsx.produce()
