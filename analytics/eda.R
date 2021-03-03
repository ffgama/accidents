setwd(".")

library(data.table)
library(lubridate)
library(dplyr)

FULL_PATH_FILE = "etl_files/data/pre_processed_data/data_accidents.csv.gz"

data_accidents  = fread(FULL_PATH_FILE, sep=";")

data_accidents = data_accidents %>% 
  mutate_at("data_inversa", ~as_datetime(.))

# Numero de ocorrencias por ano.
# Nos ultimos 5 anos tivemos uma queda no numero de ocorrencias.
data_accidents %>%
  dplyr::mutate(year = year(data_inversa)) %>%
  group_by(year) %>%
  tally() %>%
  arrange(desc(n))

# Dia da semana mais frequentes.
# As ocorrencias estao bem distribuidas entre os dias. Com a informacao de causa do acidente ou tipo de acidente talvez
# consigamos encontrar algum fator discriminativo para esta variavel.
data_accidents %>%
  group_by(dia_semana) %>%
  tally()

# Top-15 volume de ocorrencias
# Cidades do eixo sul/sudeste detem os maiores volumes de ocorrencias. 
data_accidents %>%
  group_by(cidade_uf) %>%
  tally() %>% 
  arrange(desc(n)) %>%
  print(n=15)

count_categorical_variable = function(data, variable, print.show.rows=10){
  
  dataset = data %>%
    group_by(.data[[variable]]) %>%
    summarise(n = n()) %>%
    mutate(prop = (n/sum(n)*100)) %>%
    arrange(desc(n)) %>%
    print(n = print.show.rows)
  
}

# Causas das ocorrencias.
# Nota-se que a falta de atencao é o fator mais predominante que justificam o registro dessas ocorrencias. Quase 30%.
# Uma hipotese é que o uso do celular poderia ser um dos principais responsaveis. Podemos investigar mais tarde.
count_categorical_variable(data=data_accidents, variable="causa_acidente")

# A colisao traseira é o tipo de causa mais comum. Provavelmente em funcao dessa falta de atencao.
count_categorical_variable(data=data_accidents, variable="tipo_acidente")
