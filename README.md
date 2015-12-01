# taxonomy
For doing a taxonomy of a text (for an English class or something)

Requirements
---
* python 2.7
* pip
* docker

Steps
---
1. `git clone https://github.com/pdxjohnny/taxonomy.git`
2. `pip install -r requirements.txt`
3. Place your ascii section as all one line. No newlines. Into `section`.
4. Run `./init.sh`
5. Run the various chart creators
  1. `python -m taxonomy.sentence`
  2. `python -m taxonomy.most_used_words`
  3. `python -m taxonomy.punctuation`
  4. `python -m taxonomy.sentence_kind`
