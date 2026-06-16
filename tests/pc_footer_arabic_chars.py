"""pc footer-arabic: номер первой страницы — именно арабская '1' (не 'I', не 'a')."""
import helpers as h

c = h.Checks("pc_footer_arabic_chars")
pdf = h.compile("pc_footer_arabic_chars.typ")

foot = h.footer_word(pdf, 1)
c.check("is_arabic_one", foot == "1",
        f"номер {foot!r}, ждём арабскую '1' (не римскую/буквенную)")

# Цифры 0-9 ASCII, без латинских/римских символов.
c.check("only_ascii_digits", foot is not None and foot.isdigit() and foot.isascii(),
        f"номер {foot!r} не из ASCII-цифр")

c.done()
