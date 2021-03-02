setwd(".")

library(data.table)
library(lubridate)
library(dplyr)

FULL_PATH_FILE = "etl_files/data/pre_processed_data/data_accidents.csv.gz"

data_accidents  = fread(FULL_PATH_FILE, sep=";")

data_accidents = data_accidents %>% 
  mutate_at("data_inversa", ~as_datetime(.))

data_accidents %>% head(2)

# Numero de ocorrencias por ano.
# Nos ultimos 5 anos tivemos uma queda no numero de ocorrencias.
data_accidents %>%
  dplyr::mutate(year = year(data_inversa)) %>%
  group_by(year) %>%
  tally() %>%
  arrange(desc(n))

# Dia da semana mais frequentes
data_accidents %>%
  group_by(dia_semana) %>%
  tally()
