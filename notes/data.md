# `data/uz_wiki.txt` — korpus tahlili

Manba: `wikimedia/wikipedia`, `20231101.uz` (HF datasets, streaming), `src/download_data.py`.
Filtr: 200 belgidan qisqa maqolalar tashlab yuborilgan, 15 MB ga yetganda to'xtatilgan.

## 1. Hajm

| Ko'rsatkich | Qiymat |
|---|---|
| Maqolalar | ARTICLES_TODO |
| Hajm | 15.0 MB (15 737 917 bayt), 15.1 mln belgi |
| So'zlar (`split()`) | 1 853 022 |
| Noyob so'zlar | 318 941 |
| Qatorlar | 143 004 (bo'sh emas: 95 506) |

Noyob so'zlar ko'p (~17%), chunki o'zbek tili agglyutinativ: `kitob`, `kitobim`, `kitoblarimizdan`
alohida so'z sanaladi. Aynan shu narsa BPE subword'lari foydali ekanini ko'rsatadi.

## 2. Yozuv: lotin yoki kirill?

Deyarli butunlay **lotin**:

- Lotin harflari: 11.78 mln, kirill harflari: 0.22 mln → kirill ulushi **~1.9%**.
- Kirill asosan qatorlari: 3 895 ta. Ko'pi ruscha manba nomlari
  (`Большая советская энциклопедия`, `Успехи физических наук (ruscha)`) va bitta harfli ro'yxat sarlavhalari (`Д`, `Г`).
- Bitta so'z ichida aralash yozuv: 596 ta so'z. Bular xato: lotin so'z ichida kirillcha
  ko'rinishi bir xil harf bor, masalan `Arxеologiya`, `muzеyi`, `yеtkazib` (kirillcha `е`),
  `аrbobi` (kirillcha `а`), `eъlon`, `isteъfoga` (`ъ` apostrof o'rnida), `bӯyicha` (tojikcha `ӯ`).

Xulosa: kirill matn uchun bu korpus deyarli hech narsa bermaydi. Bu korpusda o'qitilgan tokenizer
`uz_cyrl` gaplarda yomon natija berishi kutiladi. Kirill uchun alohida korpus yoki transliteratsiya kerak.

## 3. Apostrof qaysi belgi bilan?

`o`/`O`/`g`/`G` dan keyingi belgi bo'yicha (~173 ming holat):

| Belgi | Unicode | Soni | Ulushi |
|---|---|---|---|
| `oʻ` | U+02BB MODIFIER LETTER TURNED COMMA | 159 938 | **~92%** |
| `o'` | U+0027 APOSTROPHE (ASCII) | 7 291 | ~4% |
| `o‘` | U+2018 LEFT SINGLE QUOTATION MARK | 4 455 | ~3% |
| `o’` | U+2019 RIGHT SINGLE QUOTATION MARK | 1 003 | ~0.6% |
| `` o` `` | U+0060 GRAVE ACCENT | 474 | ~0.3% |
| `oʼ` / `o´` | U+02BC / U+00B4 | 142 | ~0.1% |

Tutuq belgisi (`eʼlon`, `maʼlumot`) uchun asosan **U+02BC `ʼ`** ishlatilgan (22 680 ta).
Bu rasmiy imlo bilan mos: `oʻ`/`gʻ` uchun U+02BB, tutuq uchun U+02BC.

**Nega muhim:** tokenizer uchun `oʻ`, `o'`, `o‘` uch xil bayt ketma-ketligi
(`ʻ` UTF-8 da 2 bayt, `'` 1 bayt). Natijada:

- Bitta so'z (`koʻp` / `ko'p` / `ko‘p`) uch xil tokenlarga bo'linadi va BPE merge'lari uch qismga taqsimlanadi.
- **`data/test_sentences.json` ASCII `'` ishlatadi, korpus esa `ʻ` ishlatadi.** Shunday qolsa,
  o'zimizning tokenizer test gaplarda keraksiz yomon natija ko'rsatadi.
  Yechim: o'qitishdan oldin ham, testdan oldin ham apostroflarni bitta shaklga normalizatsiya qilish
  (masalan, `' ‘ ’ ` ´` → `ʻ` `o`/`g` dan keyin, qolgan joylarda → `ʼ`). Yoki test gaplarni korpusga moslash.

## 4. "Axlat"

| Turi | Miqdori | Misol |
|---|---|---|
| Bo'lim sarlavhalari (qisqa qatorlar < 25 belgi) | 37 593 qator | `Manbalar` (2 231), `Havolalar` (1 971), `Voqealar`, `Vafot etganlar` |
| Raqamga to'la qatorlar (> 30% raqam) | 2 487 qator | `Chust — 71 200,`, `o‘zbeklar - 1801896 yoki 92,54%` |
| Raqamlar umuman | belgilarning 2.4% | sanalar, aholi soni, yillar |
| Wiki/kod qoldiqlari | ~388 qator | `[[Turkum:Xitoy tillari]`, Prolog/Ruby kod parchalari |
| Inglizcha bo'laklar | ~189 qator | adabiyot ro'yxatlari: `Soviet Disunion: A History of ...` |
| NO-BREAK SPACE (U+00A0) | 21 890 ta | raqamlar ichida (`71 200`) — `split()` bunda ham bo'ladi |
| Har xil qo'shtirnoq/chiziq | `“ „ « » — –` | bir ma'no uchun bir necha belgi |

Umumiy baho: korpus nisbatan **toza**, jadval va HTML qoldiqlari kam (HF versiyasi wiki-markup'dan
tozalangan). Asosiy shovqin: `Manbalar`/`Havolalar` kabi takrorlanuvchi sarlavhalar, raqamli ro'yxatlar
va ingliz/rus tilidagi adabiyot ro'yxatlari.

## Keyingi qadam uchun xulosalar

1. Apostrofni normalizatsiya qilish, bu eng katta ta'sir.
2. Kirill uchun ma'lumot deyarli yo'q, natijalarda buni hisobga olish kerak.
3. Ixtiyoriy: `Manbalar`/`Havolalar` dan keyingi qismni kesib tashlash (asosan inglizcha/ruscha havolalar).
4. Ixtiyoriy: U+00A0 ni oddiy bo'sh joyga almashtirish.
