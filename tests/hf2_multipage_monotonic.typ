#import "../gost732-2017/g7.32-2017.typ": *
#show: гост732-2017

#for i in range(1, 12) {
  [Страница номер #i содержит немного текста.]
  if i < 11 { pagebreak() }
}
