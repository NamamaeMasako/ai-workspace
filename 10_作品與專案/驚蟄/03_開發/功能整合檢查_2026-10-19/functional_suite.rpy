# External native tests; copied only into the isolated test game by run_checks.py.
init 990 python:
    import os as _qa_os
    import json as _qa_json
    import time as _qa_time
    from pathlib import Path as _qa_Path
    _qa_output = _qa_Path(_qa_os.environ['JZ_QA_OUTPUT'])
    _test.screenshot_directory = str(_qa_output / 'screenshots')
    _test.timeout = 15.0
    config.debug_sound = True
    renpy.music.register_channel("qa_decode", mixer="sfx", loop=False)
    renpy.music.set_volume(0.0, channel="qa_decode")

    def _qa_record(kind, **details):
        details.update(kind=kind, time=_qa_time.time(), location=renpy.get_filename_line())
        with (_qa_output / 'events.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(_qa_json.dumps(details, ensure_ascii=False) + '\n')

    def _qa_label(label, abnormal):
        if label in ('start', 'prologue', 'end_game', 'jz_ending_flow') or label.startswith('chapter_'):
            _qa_record('label', label=label, replay=bool(_in_replay))
    config.label_callbacks.append(_qa_label)

    def _qa_line(event, **kwargs):
        if event == 'begin':
            _qa_record('dialogue', name=save_name, replay=bool(_in_replay),
                       music=renpy.music.get_playing(channel='music'),
                       ambience=renpy.music.get_playing(channel='ambience'))
    config.all_character_callbacks.append(_qa_line)

    _qa_status_time = 0.0
    def _qa_status():
        global _qa_status_time
        if renpy.test.testexecution.initialized and not renpy.test.testexecution.is_in_test():
            renpy.quit(status=1 if renpy.test.testreporter.reporter.has_failed else 0)
        if _qa_time.time() - _qa_status_time < 1:
            return
        _qa_status_time = _qa_time.time()
        node = renpy.test.testexecution.node_executor.node
        data = dict(location=renpy.get_filename_line(), test_node=type(node).__name__,
                    test_line=getattr(node, 'linenumber', None), save_name=save_name,
                    screens=[name for name in ('main_menu', 'choice', 'save', 'jz_chapter_replay', 'jz_ending_credits', 'jz_ending_complete') if renpy.get_screen(name)])
        (_qa_output / 'status.json').write_text(_qa_json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    config.periodic_callback = _qa_status

    def _qa_run_once(key, action):
        # Loading restarts the game context before the native test Action can
        # advance its instruction; an external marker prevents re-loading forever.
        if _qa_os.environ.get('JZ_QA_ACTION_ONCE') != key:
            _qa_os.environ['JZ_QA_ACTION_ONCE'] = key
            action()

testsuite jz_qa:
    testcase defaults:
        assert screen "main_menu" timeout 5
        assert eval (not jz_replay_unlocked()) timeout 5
        assert eval (preferences.skip_unseen == False) timeout 5
        assert eval (preferences.skip_after_choices == False) timeout 5
        assert eval (preferences.transitions == 2) timeout 5
        assert eval (jz_dialogue_size() == 34 and jz_textbox_alpha() == 1.0) timeout 5
        click "設定"
        assert "閱讀設定" timeout 5
        screenshot "settings_defaults.png"
        click "返回"
        assert screen "main_menu" timeout 5

    testcase hanami_first:
        click "開始遊戲"
        advance until screen "choice" timeout 240
        assert eval (first_route is None and second_route is None) timeout 5
        assert eval (save_name == '第七章・錯路\n第一次交卡：選擇前') timeout 5
        run FileTakeScreenshot()
        run FileSave(1, page="9", confirm=False)
        assert eval (FileSaveName(1, page="9") == save_name) timeout 5
        click "交給花見"
        assert eval (first_route == 'hanami') timeout 5
        assert eval (save_name == '第七章・錯路\n第一次交卡：花見') timeout 5
        run Function(_qa_run_once, "manual_load", FileLoad(1, page="9", confirm=False))
        assert screen "choice" timeout 5
        assert eval (first_route is None and second_route is None) timeout 5
        assert eval (save_name == '第七章・錯路\n第一次交卡：選擇前') timeout 5
        click "交給花見"
        run QuickSave(message="QA")
        assert eval (FileSaveName(1, page="quick") == save_name) timeout 5
        advance repeat 4
        run Function(_qa_run_once, "quick_load", QuickLoad(confirm=False))
        assert eval (save_name == '第七章・錯路\n第一次交卡：花見') timeout 5
        click "存檔"
        run FilePage("9")
        screenshot "save_chapter_and_route.png"
        click "返回"
        advance until eval (save_name == '第七章・錯路\n第二次交卡：夢見') timeout 180
        assert eval (second_route == 'yumemi') timeout 5
        assert eval (save_name == '第七章・錯路\n第二次交卡：夢見') timeout 5
        advance until eval (save_name == '第八章・春雷\n最後的選擇') timeout 180
        advance until screen "choice" timeout 30
        click "把卡留給自己"
        assert eval (save_name == '第八章・春雷\n把卡留給自己') timeout 5
        advance until screen "jz_ending_credits" timeout 180
        assert eval (save_name == '第八章・春雷\n製作名單') timeout 5
        screenshot "credits.png"
        pause until screen "jz_ending_complete" timeout 45
        assert eval (persistent.jz_completed and jz_replay_unlocked()) timeout 5
        assert eval (save_name == '第八章・春雷\n完') timeout 5
        screenshot "ending.png"
        click "返回主選單"
        assert screen "main_menu" timeout 5

    testcase yumemi_first:
        click "開始遊戲"
        advance until screen "choice" timeout 240
        assert eval (first_route is None and second_route is None) timeout 5
        click "交給夢見"
        assert eval (first_route == 'yumemi') timeout 5
        assert eval (save_name == '第七章・錯路\n第一次交卡：夢見') timeout 5
        advance until eval (save_name == '第七章・錯路\n第二次交卡：花見') timeout 180
        assert eval (second_route == 'hanami') timeout 5
        assert eval (save_name == '第七章・錯路\n第二次交卡：花見') timeout 5
        advance until eval (save_name == '第八章・春雷\n最後的選擇') timeout 180
        advance until screen "choice" timeout 30
        click "把卡留給自己"
        advance until screen "jz_ending_credits" timeout 180
        click "略過製作名單"
        assert screen "jz_ending_complete" timeout 5
        click "返回主選單"
        assert screen "main_menu" timeout 5

    testcase replay_chapters:
        parameter key = ['prologue', 'chapter_1', 'chapter_2', 'chapter_3', 'chapter_4', 'chapter_5', 'chapter_6', 'chapter_7', 'chapter_8']
        click "章節回看"
        if eval (key == 'prologue'):
            click "月下庄"
        elif eval (key == 'chapter_1'):
            click "留宿"
        elif eval (key == 'chapter_2'):
            click "煙與孤影"
        elif eval (key == 'chapter_3'):
            click "黑卡"
        elif eval (key == 'chapter_4'):
            click "蛛影"
        elif eval (key == 'chapter_5'):
            click "牽絲"
        elif eval (key == 'chapter_6'):
            click "先手"
        elif eval (key == 'chapter_7'):
            click "錯路"
        else:
            click "春雷"
        assert eval (bool(_in_replay)) timeout 5
        assert eval (not FileSave(1).get_sensitive()) timeout 5
        if eval (key == 'chapter_7'):
            advance until screen "choice" timeout 30
            click "交給花見"
        if eval (key == 'chapter_8'):
            advance until screen "choice" timeout 30
            click "把卡留給自己"
            advance until screen "jz_ending_credits" timeout 180
            click "略過製作名單"
            assert "返回章節回看" timeout 5
            click "返回章節回看"
        else:
            advance until screen "jz_chapter_replay" timeout 180
        assert eval (not _in_replay) timeout 5
        assert screen "jz_chapter_replay" timeout 5
        assert eval (renpy.music.get_playing(channel='music') == config.main_menu_music) timeout 5
        click "返回"
        assert screen "main_menu" timeout 5

    testcase legacy_load:
        parameter slot = ['legacy-1', 'legacy-2']
        run Function(_qa_run_once, slot, FileLoad(slot, slot=True, confirm=False))
        assert eval (not main_menu) timeout 5
        if "交給花見":
            click "交給花見"
        elif "把卡留給自己":
            click "把卡留給自己"
        else:
            advance
        if "交給花見":
            click "交給花見"
        elif "把卡留給自己":
            click "把卡留給自己"
        else:
            advance
        if "交給花見":
            click "交給花見"
        elif "把卡留給自己":
            click "把卡留給自己"
        else:
            advance
        run FileTakeScreenshot()
        run FileSave(1, page="8", confirm=False)
        assert eval (FileLoad(1, page='8').get_sensitive()) timeout 5
        run Function(_qa_run_once, "menu_" + slot, MainMenu(confirm=False))
        assert screen "main_menu" timeout 5

testcase jz_prefs_write:
    click "設定"
    click "小"
    run SetField(persistent, "jz_textbox_opacity", 0.2)
    assert eval (jz_dialogue_size() == 26 and jz_textbox_alpha() == 0.2) timeout 5
    $ renpy.save_persistent()
    click "返回"

testcase jz_prefs_read:
    assert eval (jz_dialogue_size() == 26 and jz_textbox_alpha() == 0.2) timeout 5
    assert eval (jz_replay_unlocked()) timeout 5
    click "設定"
    click "中"
    run SetField(persistent, "jz_textbox_opacity", 0.6)
    assert eval (jz_dialogue_size() == 30 and jz_textbox_alpha() == 0.6) timeout 5
    click "大（原始字級）"
    run SetField(persistent, "jz_textbox_opacity", 1.0)
    $ renpy.save_persistent()
    click "返回"

testcase jz_replay_early_exit:
    $ _qa_os.environ['JZ_QA_OUTER'] = _qa_json.dumps([getattr(renpy.store, 'first_route', None), getattr(renpy.store, 'second_route', None), save_name])
    click "章節回看"
    click "留宿"
    assert eval (bool(_in_replay)) timeout 5
    click "設定"
    click "結束回放"
    click "是"
    assert eval (not _in_replay) timeout 5
    assert screen "jz_chapter_replay" timeout 5
    assert eval (_qa_json.dumps([getattr(renpy.store, 'first_route', None), getattr(renpy.store, 'second_route', None), save_name]) == _qa_os.environ['JZ_QA_OUTER']) timeout 5
    screenshot "replay_return.png"
    click "返回"
    assert screen "main_menu" timeout 5

testcase jz_controls:
    click "開始遊戲"
    advance until eval (save_name == '序章・月下庄') timeout 30
    advance repeat 3
    $ _qa_os.environ['JZ_QA_ROLLBACK_FROM'] = str(renpy.get_filename_line()[1])
    keysym "rollback"
    pause 0.3
    assert eval (renpy.get_filename_line()[1] < int(_qa_os.environ['JZ_QA_ROLLBACK_FROM'])) timeout 5
    advance repeat 2
    click "歷史"
    assert screen "history" timeout 5
    screenshot "history.png"
    click "返回"
    $ _qa_afm_from = renpy.get_filename_line()
    run Preference("auto-forward time", 1)
    run Preference("auto-forward", "enable")
    pause 3.0
    run Preference("auto-forward", "disable")
    assert eval (renpy.get_filename_line() != _qa_afm_from) timeout 5
    $ renpy.force_autosave(take_screenshot=True, block=True)
    assert eval (FileLoad(1, page='auto').get_sensitive()) timeout 5
    assert eval (bool(FileSaveName(1, page='auto'))) timeout 5
    run Preference("skip", "all")
    skip until screen "choice" timeout 150
    assert eval (first_route is None and second_route is None) timeout 5
    assert eval (preferences.skip_after_choices == False) timeout 5
    run Preference("skip", "seen")
    click "設定"
    run Preference("transitions", "none")
    assert eval (preferences.transitions == 0) timeout 5
    run Preference("transitions", "all")
    assert eval (preferences.transitions == 2) timeout 5
    run Preference("display", "fullscreen")
    pause 0.5
    assert eval (preferences.fullscreen) timeout 5
    run Preference("display", "window")
    pause 0.5
    assert eval (not preferences.fullscreen) timeout 5
    screenshot "settings_controls.png"
    click "主選單"
    click "是"
    assert screen "main_menu" timeout 5

testcase jz_render_assets:
    python:
        _qa_rendered = []
        for _qa_image_name, _qa_image in sorted(renpy.display.image.images.items()):
            if _qa_image_name[0] in ('bg', 'cg', 'event', 'jingzhe', 'hanami', 'yumemi', 'achirichi', 'shadow_witch', 'kamikiri', 'omukade', 'jorogumo', 'tsuchigumo'):
                renpy.render(_qa_image, 1280, 720, 0, 0)
                _qa_rendered.append(' '.join(_qa_image_name))
        _qa_record('rendered_assets', names=_qa_rendered)
    assert eval (len(_qa_rendered) >= 80) timeout 5


testcase jz_audio_decode:
    parameter filename = ['audio/ambience/amb_courtyard_water_wind.ogg', 'audio/ambience/amb_inn_wood_room.ogg', 'audio/ambience/amb_road_twilight_wind.ogg', 'audio/music/bgm_before_storm.ogg', 'audio/music/bgm_black_card_memory.ogg', 'audio/music/bgm_black_card_memory_variant.ogg', 'audio/music/bgm_choose_my_fate.ogg', 'audio/music/bgm_dawn_together.ogg', 'audio/music/bgm_forest_assault.ogg', 'audio/music/bgm_hold_on.ogg', 'audio/music/bgm_inn_hunted.ogg', 'audio/music/bgm_lantern_theme.ogg', 'audio/music/bgm_loss_and_rewind.ogg', 'audio/music/bgm_moon_inn_day.ogg', 'audio/music/bgm_moon_inn_night.ogg', 'audio/music/bgm_road_to_moon_inn.ogg', 'audio/music/bgm_shadow_witch.ogg', 'audio/music/bgm_silk_under_door.ogg', 'audio/sfx/battle/battle_body_fall_soft.ogg', 'audio/sfx/battle/battle_body_hit_dull.ogg', 'audio/sfx/battle/battle_cough_blood.ogg', 'audio/sfx/battle/battle_kamikiri_blades.ogg', 'audio/sfx/battle/battle_naginata_armor_hit.ogg', 'audio/sfx/battle/battle_naginata_whoosh.ogg', 'audio/sfx/battle/battle_omukade_armor_move.ogg', 'audio/sfx/battle/battle_omukade_impact.ogg', 'audio/sfx/battle/battle_silk_cut.ogg', 'audio/sfx/battle/battle_silk_snap_fine.ogg', 'audio/sfx/battle/battle_silk_whisper.ogg', 'audio/sfx/battle/battle_spider_steps.ogg', 'audio/sfx/battle/battle_spider_steps_heavy.ogg', 'audio/sfx/battle/battle_tsuchigumo_hiss.ogg', 'audio/sfx/magic/magic_black_card_pulse.ogg', 'audio/sfx/magic/magic_black_card_pulse_hold.ogg', 'audio/sfx/magic/magic_black_card_tear.ogg', 'audio/sfx/magic/magic_insect_summon.ogg', 'audio/sfx/magic/magic_kiseru_blow.ogg', 'audio/sfx/magic/magic_kiseru_draw.ogg', 'audio/sfx/magic/magic_kiseru_ember.ogg', 'audio/sfx/magic/magic_kiseru_ignite.ogg', 'audio/sfx/magic/magic_mailbox_close.ogg', 'audio/sfx/magic/magic_mailbox_open.ogg', 'audio/sfx/magic/magic_mailbox_reveal.ogg', 'audio/sfx/magic/magic_night_rift.ogg', 'audio/sfx/ui/ui_back.ogg', 'audio/sfx/ui/ui_confirm.ogg', 'audio/sfx/world/world_black_card_place.ogg', 'audio/sfx/world/world_black_card_slide.ogg', 'audio/sfx/world/world_black_card_stow.ogg', 'audio/sfx/world/world_cloth_drag_soft.ogg', 'audio/sfx/world/world_cloth_soft.ogg', 'audio/sfx/world/world_cloth_wrapped_naginata.ogg', 'audio/sfx/world/world_door_knock_soft.ogg', 'audio/sfx/world/world_dry_material_rub.ogg', 'audio/sfx/world/world_footstep_wet.ogg', 'audio/sfx/world/world_footstep_wood.ogg', 'audio/sfx/world/world_frame_thud_soft.ogg', 'audio/sfx/world/world_herb_crush.ogg', 'audio/sfx/world/world_lamp_drop.ogg', 'audio/sfx/world/world_lamp_sway.ogg', 'audio/sfx/world/world_mailbox_stow.ogg', 'audio/sfx/world/world_notebook_close.ogg', 'audio/sfx/world/world_notebook_open.ogg', 'audio/sfx/world/world_paper_fold.ogg', 'audio/sfx/world/world_sliding_door.ogg', 'audio/sfx/world/world_sliding_door_close_soft.ogg', 'audio/sfx/world/world_table_tap_double.ogg', 'audio/sfx/world/world_window_slide_soft.ogg', 'audio/sfx/world/world_wood_bell.ogg', 'audio/sfx/world/world_writing_pen.ogg']
    run Function(renpy.music.play, filename, channel="qa_decode", loop=False)
    pause 0.15
    assert eval (renpy.music.get_duration(channel="qa_decode") > 0) timeout 3
    $ _qa_record("audio_decoded", filename=filename, duration=renpy.music.get_duration(channel="qa_decode"))
    run Function(renpy.music.stop, channel="qa_decode")
