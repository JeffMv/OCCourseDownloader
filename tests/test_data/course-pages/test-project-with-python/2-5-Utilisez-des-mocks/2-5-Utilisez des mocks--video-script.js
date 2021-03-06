
    (function(document, player) {
        /* global TextTrackList, ActiveXObject, VimeoPlayer */

        var config = {"cdn_url":"https://f.vimeocdn.com","vimeo_api_url":"api.vimeo.com","request":{"files":{"dash":{"separate_av":true,"streams":[{"profile":119,"quality":"1080p","id":753898737,"fps":25},{"profile":174,"quality":"720p","id":753898733,"fps":25},{"profile":165,"quality":"540p","id":753898738,"fps":25},{"profile":164,"quality":"360p","id":753898728,"fps":25}],"cdns":{"akfire_interconnect_quic":{"url":"https://70skyfiregce-vimeo.akamaized.net/exp=1566234414~acl=%2F217633069%2F%2A~hmac=a7bd4c105ac4352979551cc7534ca5ab59d14413247216bac83431317db96f6d/217633069/sep/video/753898728,753898738,753898737,753898733/master.json?base64_init=1","origin":"gcs"},"fastly_skyfire":{"url":"https://skyfire.vimeocdn.com/1566234414-0x4bbcec2a620b3ad168e5ff0109b900bbd115c294/217633069/sep/video/753898728,753898738,753898737,753898733/master.json?base64_init=1","origin":"gcs"}},"default_cdn":"akfire_interconnect_quic"},"hls":{"separate_av":false,"default_cdn":"akfire_interconnect_quic","cdns":{"akfire_interconnect_quic":{"url":"https://70skyfiregce-vimeo.akamaized.net/exp=1566234414~acl=%2F217633069%2F%2A~hmac=a7bd4c105ac4352979551cc7534ca5ab59d14413247216bac83431317db96f6d/217633069/video/753898728,753898738,753898737,753898733/subtitles/5019129-Fran%C3%A7ais-fr/master.m3u8?external-subs=1","origin":"gcs","captions":"https://70skyfiregce-vimeo.akamaized.net/exp=1566234414~acl=%2F217633069%2F%2A~hmac=a7bd4c105ac4352979551cc7534ca5ab59d14413247216bac83431317db96f6d/217633069/video/753898728,753898738,753898737,753898733/subtitles/5019129-Fran%C3%A7ais-fr/master.m3u8"},"fastly_skyfire":{"url":"https://skyfire.vimeocdn.com/1566234414-0x4bbcec2a620b3ad168e5ff0109b900bbd115c294/217633069/video/753898728,753898738,753898737,753898733/subtitles/5019129-Fran%C3%A7ais-fr/master.m3u8?external-subs=1","origin":"gcs","captions":"https://skyfire.vimeocdn.com/1566234414-0x4bbcec2a620b3ad168e5ff0109b900bbd115c294/217633069/video/753898728,753898738,753898737,753898733/subtitles/5019129-Fran%C3%A7ais-fr/master.m3u8"}},"captions":"https://70skyfiregce-vimeo.akamaized.net/exp=1566234414~acl=%2F217633069%2F%2A~hmac=a7bd4c105ac4352979551cc7534ca5ab59d14413247216bac83431317db96f6d/217633069/video/753898728,753898738,753898737,753898733/subtitles/5019129-Fran%C3%A7ais-fr/master.m3u8"},"progressive":[{"profile":165,"width":960,"mime":"video/mp4","fps":25,"url":"https://gcs-vimeo.akamaized.net/exp=1566234414~acl=%2A%2F753898738.mp4%2A~hmac=5f1cec6db71e189ef38d6f47eb35e60be96bf21717f0ba1b39af3f551d26fa45/vimeo-prod-skyfire-std-us/01/3526/8/217633069/753898738.mp4","cdn":"akamai_interconnect","quality":"540p","id":753898738,"origin":"gcs","height":540},{"profile":119,"width":1920,"mime":"video/mp4","fps":25,"url":"https://gcs-vimeo.akamaized.net/exp=1566234414~acl=%2A%2F753898737.mp4%2A~hmac=d16fb334b0ba40bc15c910e8763c2146a8c0588a1616a3553d3a66b4cd0a7df1/vimeo-prod-skyfire-std-us/01/3526/8/217633069/753898737.mp4","cdn":"akamai_interconnect","quality":"1080p","id":753898737,"origin":"gcs","height":1080},{"profile":174,"width":1280,"mime":"video/mp4","fps":25,"url":"https://gcs-vimeo.akamaized.net/exp=1566234414~acl=%2A%2F753898733.mp4%2A~hmac=37b935c49b2b927eae8e9d9b76abeb3ae9a96b5b3b9344d46053e7680a5c1897/vimeo-prod-skyfire-std-us/01/3526/8/217633069/753898733.mp4","cdn":"akamai_interconnect","quality":"720p","id":753898733,"origin":"gcs","height":720},{"profile":164,"width":640,"mime":"video/mp4","fps":25,"url":"https://gcs-vimeo.akamaized.net/exp=1566234414~acl=%2A%2F753898728.mp4%2A~hmac=0554051e7fa3ebb6ceb9373d04bf40c5d62e8f909c6469e37956e766a3064294/vimeo-prod-skyfire-std-us/01/3526/8/217633069/753898728.mp4","cdn":"akamai_interconnect","quality":"360p","id":753898728,"origin":"gcs","height":360}]},"lang":"en","sentry":{"url":"https://6f5f8e1cecfa40fb850f578b69fc1705@sentry.io/1297650","enabled":false,"debug_enabled":true,"debug_intent":0},"ab_tests":{"chromecast":{"data":{},"group":false},"cdn_preference":{"data":{"city":"ch\u00e2tel","country_code":"FR","hls_pref_found":false,"dash_pref_found":false},"group":false}},"referrer":null,"cookie_domain":".vimeo.com","timestamp":1566230514,"gc_debug":{"bucket":"vimeo-player-debug"},"expires":3600,"text_tracks":[{"lang":"fr","url":"/texttrack/5019129.vtt?token=5d5ad602_0x51e085abd72e3170457ac1c4fa488d147fd7d96a","kind":"subtitles","id":5019129,"label":"Fran\u00e7ais"}],"currency":"EUR","session":"3e60b953fda89122a73b55cb99f0ee011885f7ec1566230514","cookie":{"scaling":1,"volume":1.0,"quality":null,"hd":0,"captions":null},"build":{"backend":"1.9.1","js":"3.14.24"},"urls":{"barebone_js":"https://f.vimeocdn.com/p/3.14.24/js/barebone.js","zeroclip_swf":"https://f.vimeocdn.com/p/external/zeroclipboard/ZeroClipboard.swf","fresnel":"https://fresnel.vimeocdn.com/add/player-stats","js":"https://f.vimeocdn.com/p/3.14.24/js/player.js","proxy":"https://player.vimeo.com/static/proxy.html","chromeless_css":"https://f.vimeocdn.com/p/3.14.24/css/chromeless.css","fresnel_chunk_url":"https://fresnel-events.vimeocdn.com/add/chunk_downloads","three_js":"https://f.vimeocdn.com/p/external/three.rvimeo.min.js","sentry_url":"https://f.vimeocdn.com/p/external/sentry.min.js","mux_url":"https://f.vimeocdn.com/p/external/mux.js","vuid_js":"https://f.vimeocdn.com/js_opt/modules/utils/vuid.min.js","chromeless_js":"https://f.vimeocdn.com/p/3.14.24/js/chromeless.js","zeroclip_js":"https://f.vimeocdn.com/p/external/zeroclipboard/ZeroClipboard-patch.js","css":"https://f.vimeocdn.com/p/3.14.24/css/player.css"},"signature":"39dcd44968163d40b9639a424f77c368","flags":{"preload_video":"metadata_on_hover","plays":1,"log":0,"dnt":0,"partials":1,"autohide_controls":0},"country":"FR","file_codecs":{"hevc":{"hdr":[],"sdr":[]},"av1":[],"avc":[753898738,753898737,753898733,753898728]}},"player_url":"player.vimeo.com","video":{"rating":{"id":6},"version":{"current":null,"available":[]},"height":1080,"duration":568,"thumbs":{"1280":"https://i.vimeocdn.com/video/634901663_1280.jpg","960":"https://i.vimeocdn.com/video/634901663_960.jpg","640":"https://i.vimeocdn.com/video/634901663_640.jpg","base":"https://i.vimeocdn.com/video/634901663"},"owner":{"account_type":"business","name":"OpenClassrooms","img":"https://i.vimeocdn.com/portrait/28786337_60x60.jpg","url":"https://vimeo.com/openclassrooms","img_2x":"https://i.vimeocdn.com/portrait/28786337_120x120.jpg","id":19604204},"file_codecs":{"hevc":{"hdr":[],"sdr":[]},"av1":[],"avc":[753898738,753898737,753898733,753898728]},"id":217633069,"embed_code":"<iframe title=\"vimeo-player\" src=\"https://player.vimeo.com/video/217633069\" width=\"640\" height=\"360\" frameborder=\"0\" allowfullscreen><\/iframe>","title":"FR_4425126_testez-un-projet-python_P2C5","share_url":"https://vimeo.com/217633069","width":1920,"embed_permission":"public","fps":25.0,"spatial":0,"live_event":null,"allow_hd":1,"hd":1,"lang":null,"default_to_hd":1,"url":"https://vimeo.com/217633069","privacy":"anybody","bypass_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjbGlwX2lkIjoyMTc2MzMwNjksImV4cCI6MTU2NjIzMjE0MH0.cA25Y_y2EbXCtJ4qKg2SoePBRKMxi8TEFMgp1QsCbH8","unlisted_hash":null},"user":{"team_origin_user_id":0,"liked":0,"account_type":"none","vimeo_api_client_token":null,"vimeo_api_interaction_tokens":null,"team_id":0,"watch_later":0,"owner":0,"id":0,"mod":0,"logged_in":0},"embed":{"autopause":1,"playsinline":1,"settings":{"fullscreen":1,"byline":0,"like":0,"playbar":1,"title":0,"color":0,"speed":1,"watch_later":0,"share":0,"scaling":1,"spatial_compass":0,"collections":0,"info_on_pause":0,"portrait":0,"logo":0,"embed":0,"badge":0,"spatial_label":0,"volume":1},"color":"7451eb","texttrack":"","on_site":0,"app_id":"","muted":0,"dnt":0,"player_id":"","api":null,"editor":false,"context":"embed.main","time":0,"outro":"beginning","log_plays":1,"quality":null,"transparent":1,"loop":0,"autoplay":0},"view":1,"vimeo_url":"vimeo.com"};

        if (!config.request) {
            // console.error('Invalid config');
            return;
        }

        if (typeof config.request === 'object' && 'error' in config.request) {
            if ('html' in config.request) {
                document.documentElement.innerHTML = config.request.html.replace(/&lt;/g, '<').replace(/&gt;/g, '>');
            }
            return;
        }

        // This probably won't be needed, but we have frame origin set to only
        // allow pages loaded from player.vimeo.com so if this is inside of an
        // iframe we should not try to redirect to the vimeo.com url.
        //
        // We should only redirect if the player.vimeo.com/video/123 URL is
        // requested directly.
        //
        // @see http://stackoverflow.com/questions/326069/how-to-identify-if-a-webpage-is-being-loaded-inside-an-iframe-or-directly-into-t
        var isIframe = (function() {
            try {
                return window.self !== window.top;
            } catch (e) {
                return true;
            }
        }());

        // Redirect to the mobile site when player is loaded via the twitter app
        // for iOS (and Android?).  This is so we can leverage the mobile site's
        // outro in these cases and provide a tweet button.
        if (!isIframe && /twitter/i.test(navigator.userAgent) && config.video.url) {
            window.location = config.video.url;
        }

    // i18n ______________________________________________________
        if (config.request.lang) {
            document.documentElement.setAttribute('lang', config.request.lang);
        }

    // Support tests ______________________________________________________

        // Check all the prefixed versions of the fullscreen api for support.
        var fullscreenSupport = 'exitFullscreen' in document || 'webkitExitFullscreen' in document || 'webkitCancelFullScreen' in document || 'mozCancelFullScreen' in document || 'msExitFullscreen' in document || 'webkitEnterFullScreen' in document.createElement('video');

        // Check for h264 and text track support.
        var videoSupport = (function() {
            var video = document.createElement('video');

            return {
                h264: 'canPlayType' in video && video.canPlayType('video/mp4') !== '',
                textTracks: typeof TextTrackList !== 'undefined' && typeof video.textTracks !== 'undefined' && video.textTracks instanceof TextTrackList
            };
        }());

        // Does this browser support inlining SVG into HTML?
        // From modernizr: https://github.com/Modernizr/Modernizr/blob/master/feature-detects/svg/inline.js
        var inlineSvgSupport = (function() {
            var div = document.createElement('div');
            div.innerHTML = '<svg/>';
            return (div.firstChild && div.firstChild.namespaceURI) === 'http://www.w3.org/2000/svg';
        }());

        // Put Windows phone through.
        var windowsPhone = /MSIE 9/.test(navigator.userAgent) && /Windows Phone/.test(navigator.userAgent);
        var IE10 = /IE 10/.test(navigator.userAgent);


    // Initialization _____________________________________________________

        /**
         * We want to use the player if:
         *   1. The browser has fullscreen support, regardless of if it’s enabled,
         *   2. IE10 with no Flash support,
         *   3. Windows Phone
         */
        var usePlayer = fullscreenSupport || IE10 || windowsPhone;

        // We'll be inserting both the stylesheet and javascript before this script
        var firstScript = document.getElementsByTagName('script')[0];
        var script = document.createElement('script');
        var jsDone = false;
        var playerObject = false;

        // If the browser doesn't support inline svg, don't use the player.
        if (!inlineSvgSupport) {
            usePlayer = false;
        }

        // @NOTE: Make sure this is commented out before committing. - Ryan
        // usePlayer = false;

        if (!usePlayer) {
            // Remove placeholder if it exists for flash and fallback.
            // It overlaps the content.
            var placeholder = document.querySelector('.vp-placeholder');
            if (placeholder && placeholder.parentNode) {
                placeholder.parentNode.removeChild(placeholder);
            }
        }

        if (usePlayer) {
            // Add the loading class now to avoid any possibility of seeing
            // something before the player loads
            player.className = 'player loading';

            var startTime = new Date().getTime();

            // Start the loading of the javascript first
            script.src = config.request.urls.js;

            firstScript.parentNode.insertBefore(script, firstScript);
            script['onreadystatechange' in script ? 'onreadystatechange' : 'onload'] = function() {
                if (!jsDone && (!this.readyState || this.readyState === 'loaded' || this.readyState === 'complete')) {
                    jsDone = true;
                    playerObject = new VimeoPlayer(player, config, cssDone || { link: link, startTime: startTime });
                }
            };

            // Load the stylesheet
            var cssDone = false;
            var link = document.createElement('link');
            link.rel = 'stylesheet';
            // cacheBuster for ie only http://stackoverflow.com/questions/10316247/media-queries-fail-inside-ie9-iframe
            link.href = config.request.urls.css + (typeof cacheBuster === 'undefined' ? '' : cacheBuster);

            document.getElementsByTagName('head')[0].appendChild(link);
            link.onload = function() {
                cssDone = true;
            };
        }
        else {
            player.innerHTML = '<div class="fallback"><iframe title="vimeo-player" src="/video/217633069/fallback?js&amp;referrer=' + encodeURIComponent(config.request.referrer) + '" frameborder="0"></iframe></div>';
        }

        if (!config.request.flags.dnt && !config.embed.dnt) {
            window._vuid = [
                ['pid', config.request.session]
            ];
            var vim = document.createElement('script');
            vim.async = true;
            vim.src = config.request.urls.vuid_js;
            firstScript.parentNode.insertBefore(vim, firstScript);
        }

    }(document, document.getElementById('player')));
