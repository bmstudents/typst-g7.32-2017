#import "../gost732-2017/g7.32-2017.typ": *
#show: гост732-2017.with(фича-маленький-отступ-вокруг-таблиц: да)

= Раздел
Текст перед рисунком.

#рис(rect(width: 8cm, height: 4cm)[
  #align(center + top)[#text(fill: black)[ВЕРХТЕЛА]]
  #v(1fr)
  #align(center + bottom)[#text(fill: black)[НИЗТЕЛА]]
])[Подпись рисунка]

ПОСЛЕРИС текст.
