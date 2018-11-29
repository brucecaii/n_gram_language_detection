# n_gram_language_detection

To train unigram model with English corpus

```
python -m main train -n 1 -l en
```

To train unigram model with French corpus

```
python -m main train -n 1 -l fr
```

To train bigram model with English corpus

```
python -m main train -n 2 -l en
```

To train bigram model with French corpus

```
python -m main train -n 2 -l fr
```

To detect the language used as sentences with unigram

```
python -m main predict -n 1
```

To detect the language used as sentences with bigram

```
python -m main predict -n 2
```