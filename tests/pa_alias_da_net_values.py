"""pa_alias-da-net (аспект 3): да/нет — настоящие булевы алиасы (да=true, нет=false),
и все четыре фича-флага принимают да/нет одновременно без ошибок."""
import helpers as h

c = h.Checks("pa_alias_da_net_values")
pdf = h.compile("pa_alias_da_net_values.typ")
t = h.text(pdf)

# Выражение (да == true and нет == false) отрендерилось как 'true'.
c.check("da_net_are_bools", "да == true и нет == false: true" in t,
        f"да/нет не равны true/false:\n{t[:200]!r}")

# Документ с четырьмя флагами да/нет собрался.
c.check("all_flags_accepted", "Все четыре флага" in t,
        f"тело с четырьмя флагами не отрендерилось:\n{t[:200]!r}")
c.done()
