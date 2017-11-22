<?xml version="1.0" encoding="UTF-8" ?>
<Package name="samplebox-dialogflow" format_version="4">
    <Manifest src="manifest.xml" />
    <BehaviorDescriptions>
        <BehaviorDescription name="behavior" src="behavior_1" xar="behavior.xar" />
    </BehaviorDescriptions>
    <Dialogs />
    <Resources>
        <File name="VAD" src="lib/apiai/VAD.py" />
        <File name="__init__" src="lib/apiai/__init__.py" />
        <File name="apiai" src="lib/apiai/apiai.py" />
        <File name="__init__" src="lib/apiai/requests/__init__.py" />
        <File name="__init__" src="lib/apiai/requests/query/__init__.py" />
        <File name="events" src="lib/apiai/requests/query/events.py" />
        <File name="query" src="lib/apiai/requests/query/query.py" />
        <File name="text" src="lib/apiai/requests/query/text.py" />
        <File name="voice" src="lib/apiai/requests/query/voice.py" />
        <File name="request" src="lib/apiai/requests/request.py" />
        <File name="__init__" src="lib/apiai/requests/user_entities/__init__.py" />
        <File name="user_entities_request" src="lib/apiai/requests/user_entities/user_entities_request.py" />
        <File name="resampler" src="lib/apiai/resampler.py" />
        <File name="README" src="README.md" />
    </Resources>
    <Topics />
    <IgnoredPaths />
    <Translations auto-fill="en_US">
        <Translation name="translation_en_US" src="translations/translation_en_US.ts" language="en_US" />
        <Translation name="translation_ja_JP" src="translations/translation_ja_JP.ts" language="ja_JP" />
    </Translations>
</Package>
