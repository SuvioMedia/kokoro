import pytest

from kokoro import KPipeline


@pytest.mark.parametrize('lang_code', ['l', 'pl', 'pl-pl', 'PL', 'pl-PL'])
def test_polish_language_codes(lang_code):
    pipeline = KPipeline(lang_code=lang_code, model=False)

    assert pipeline.lang_code == 'l'
    assert pipeline.g2p.language == 'pl'


def test_polish_g2p_uses_only_supported_equivalents():
    pipeline = KPipeline(lang_code='pl', model=False)

    results = list(pipeline('Dźwięk, ciocia i źrebak.', split_pattern=None))

    assert len(results) == 1
    assert results[0].phonemes == 'ʥvʲˈɛŋk, ʨˈɔʨa i ʒrˈɛbak.'
    assert 'ʑ' not in results[0].phonemes
