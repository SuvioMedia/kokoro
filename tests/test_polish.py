import pytest

from kokoro import KPipeline
from kokoro.__main__ import resolve_language_and_voice


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


def test_polish_cli_defaults_to_jf_alpha():
    assert resolve_language_and_voice('l', None) == ('l', 'jf_alpha')


def test_cli_voice_defaults_remain_backwards_compatible():
    assert resolve_language_and_voice(None, None) == ('a', 'af_heart')
    assert resolve_language_and_voice('l', 'jm_kumo') == ('l', 'jm_kumo')
