from yandexfreetranslate import YandexFreeTranslate

yt = YandexFreeTranslate(api='ios')

def ru(txt):
  return yt.translate("en", "ru", txt)

def en(txt):
  return yt.translate("ru", "en", txt)
