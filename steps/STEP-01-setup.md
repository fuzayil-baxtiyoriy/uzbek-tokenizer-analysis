# 1-qadam: Loyihani sozlash va birinchi push

**Maqsad:** Desktop'dagi papka va GitHub repo bir xil bo'lsin, muhit ishlasin, README va PLAN joyida tursin.
**Vaqt:** 20–30 daqiqa

Hamma buyruqlar macOS Terminal uchun.

---

## 1.1 Papkani tayyorlash

```bash
cd ~/Desktop/uzbek-tokenizer-analysis
ls -la
```

Papka bo'sh bo'lsa yoki faqat bir nechta fayl bo'lsa, davom eting.

## 1.2 Fayllarni joylash

Yuklab olingan `uzbek-tokenizer-analysis.zip` ichidagi fayllarni shu papkaga ko'chiring:

```bash
cd ~/Downloads
unzip -o uzbek-tokenizer-analysis.zip
cp -R uzbek-tokenizer-analysis/. ~/Desktop/uzbek-tokenizer-analysis/
cd ~/Desktop/uzbek-tokenizer-analysis
```

**Kutilgan tuzilma:**

```
uzbek-tokenizer-analysis/
├── .gitignore
├── CLAUDE.md
├── PLAN.md
├── README.md
├── requirements.txt
├── data/
│   └── test_sentences.json
├── notes/
├── results/
│   └── .gitkeep
├── src/
│   ├── bpe_from_scratch.py
│   ├── compare_tokenizers.py
│   ├── pipeline.py
│   └── train_hf_tokenizer.py
└── steps/
    └── STEP-01-setup.md
```

Tekshirish:

```bash
find . -not -path "./.git*" -not -path "./.venv*" | sort
```

`notes/` bo'sh papka bo'lgani uchun git uni saqlamaydi. Shuning uchun ichiga bo'sh fayl qo'ying:

```bash
touch notes/.gitkeep
```

## 1.3 Python muhiti (venv)

```bash
python3 --version          # 3.10 yoki yangisi bo'lishi kerak
python3 -m venv .venv
source .venv/bin/activate  # terminal boshida (.venv) chiqadi
pip install --upgrade pip
pip install -r requirements.txt
```

`torch` katta kutubxona, o'rnatish bir necha daqiqa olishi mumkin.

**Tekshiruv:**

```bash
python -c "import tiktoken, tokenizers, transformers, datasets, torch, matplotlib; print('OK')"
```

`OK` chiqishi kerak.

**Eslatma:** har safar yangi terminal ochganda `source .venv/bin/activate` ni qayta yozasiz.

## 1.4 Git'ni sozlash (bir marta)

```bash
git config --global user.name "Dilshod Bakhtiyorov"
git config --global user.email "GITHUB_EMAILINGIZ"
```

## 1.5 GitHub repo

**Repo hali ochilmagan bo'lsa**, ikki usuldan birini tanlang.

**A usul: brauzerda**
1. https://github.com/new
2. Repository name: `uzbek-tokenizer-analysis`
3. Description: `How inefficient are LLM tokenizers for Uzbek? Benchmark + custom Uzbek BPE tokenizer.`
4. **Public**
5. README, .gitignore, license **qo'shmang** (ular bizda bor, konflikt bo'lmasin)
6. Create repository

**B usul: GitHub CLI (`gh`) o'rnatilgan bo'lsa**

```bash
gh auth login
gh repo create fuzayil-baxtiyoriy/uzbek-tokenizer-analysis --public \
  --description "How inefficient are LLM tokenizers for Uzbek? Benchmark + custom Uzbek BPE tokenizer."
```

**Repo allaqachon ochilgan bo'lsa** va ichida README bor bo'lsa, 1.6 dagi `git pull` qadamini bajaring.

## 1.6 Birinchi push

```bash
cd ~/Desktop/uzbek-tokenizer-analysis
git init
git branch -M main
git remote add origin https://github.com/fuzayil-baxtiyoriy/uzbek-tokenizer-analysis.git
```

Faqat repo'da GitHub yaratgan README bo'lsa:

```bash
git pull origin main --allow-unrelated-histories
# konflikt bo'lsa, bizning README'ni qoldiring:
git checkout --ours README.md
git add README.md
```

Keyin:

```bash
git status          # .venv va data/*.txt ro'yxatda BO'LMASLIGI kerak
git add .
git commit -m "Initial project structure, README, plan and setup guide"
git push -u origin main
```

Parol so'ralsa, GitHub paroli emas, **Personal Access Token** kerak:
GitHub → Settings → Developer settings → Personal access tokens → Fine-grained token → `uzbek-tokenizer-analysis` repo'ga `Contents: Read and write` ruxsati.

## 1.7 Tekshirish

- [ ] `https://github.com/fuzayil-baxtiyoriy/uzbek-tokenizer-analysis` ochiladi
- [ ] README GitHub sahifasida chiroyli ko'rinadi
- [ ] `.venv/` GitHub'da **yo'q**
- [ ] `git status` → `nothing to commit, working tree clean`
- [ ] `python -c "import torch; print(torch.__version__)"` ishlaydi

## 1.8 Repo'ni bezatish (ixtiyoriy, 2 daqiqa)

GitHub repo sahifasida o'ng tomondagi ⚙️ (About) tugmasi → **Topics**:
`nlp`, `tokenizer`, `bpe`, `uzbek`, `llm`, `pytorch`

---

## Har kungi ish tartibi (bundan keyin)

```bash
cd ~/Desktop/uzbek-tokenizer-analysis
source .venv/bin/activate
# ... ishlash ...
git add .
git commit -m "Qisqa, aniq inglizcha xabar"
git push
```

**Keyingi qadam:** `STEP-02-data.md` — o'zbekcha Wikipedia'ni yuklab olish va test gaplarini 20 taga yetkazish.
