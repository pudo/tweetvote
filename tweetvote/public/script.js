$(document).ready(function () {
    
    gStatusList = new Array();
    gCurrentStatus = 0; 
    gStatusStats = new Object();
    
    warning = function (message) {
        alert(message);
    }
    
    tweetElementId = function(elem) {
        return "tweet_" + elem.status.id;
    }
    
    indexOfId = function(tweet_id) {
        ret = -1; 
        $.each(gStatusList, function(idx, elem) {
            if (elem.status.id == tweet_id) {
                ret = idx;
            }
        });
        return ret;
    }
    
    selectElement = function(tweet_id) {
        newIdx = indexOfId(tweet_id); 
        if (newIdx == -1 || 
            newIdx < 0 || 
            newIdx >= gStatusList.length) {
            alert("stop!");
            return;
        } 
        oldSel = '#tweet_' + gCurrentStatus;
        //alert("Idx: " + newIdx + " TID: " + tweet_id + " of " + gStatusList.length);
        gCurrentStatus = tweet_id;
        $(oldSel).removeClass("current");
        newSel = '#tweet_' + tweet_id;
        $(newSel).addClass("current");
        return true;
    }
    
    followSelection = function() {
        cur = $('#tweet_' + gCurrentStatus);
        pagePart = ($(window).height()/4);
        viewportTop = $(document).scrollTop();
        scrolledPos = cur.position().top - viewportTop;
        if (scrolledPos > pagePart * 3) {
            $(document).scrollTop(viewportTop 
                + cur.outerHeight());
        } 
        if (scrolledPos < pagePart) {
            $(document).scrollTop(viewportTop    
                - cur.outerHeight());
        }
    }
    
    /* Keyboard mappings */
    $(document).keydown(function(e) {
        switch(e.which) {
            case 40: // cur down
                newIndex = indexOfId(gCurrentStatus) + 1;
                selectElement(gStatusList[newIndex].status.id); 
                followSelection();
                break;
            case 38: // cur up.
                newIndex = indexOfId(gCurrentStatus) - 1; 
                selectElement(gStatusList[newIndex].status.id); 
                followSelection();
                break;
            case 37: // cur left
                idx = indexOfId(gCurrentStatus);
                submitVote(gStatusList[idx], -1);
                break;
            case 39: // cur right
                idx = indexOfId(gCurrentStatus);
                submitVote(gStatusList[idx], 1);
                break;
            /*
            case 83:
                 $("#search_add").focus();
            */
        }
    });
    
    displayAll = function() {
        $.each(gStatusList, function(idx, elem) {
            displayElem(elem);
        });
    }
    
    displayElem = function(elem) {
        //alert(elem);
        elemId = tweetElementId(elem);
        idx = indexOfId(elem.status.id);
        elemSel = '#' + elemId
        var freshPrince = false;
        if (!$(elemSel).length) { // a new one
            freshPrince = true;
            fresh = $('#prototype').clone();
            fresh.attr('id', elemId)
            if(idx == 0) {
                fresh.insertAfter('#prototype');
            } else {
                prevId = '#' + tweetElementId(gStatusList[idx-1]);
                fresh.insertAfter(prevId);
            }
            $(elemSel + " .profile_icon").attr('src', elem.status.user.profile_image_url);
            $(elemSel + " .sender").attr('href', elem.status.user.url);
            $(elemSel + " .sender").text(elem.status.user.screen_name);
            
            text = elem.status.text;
            text = text.replace(/(http:\/\/[^ ]*)/gi, 
                '<a target="_new" href="$1">$1</a>');
            text = text.replace(/@([\w\-_]+)/gi, 
                '<a target="_new" href="http://twitter.com/$1">@$1</a>');
            text = text.replace(/#([\w\-_\.+:=]+\w)/gi, 
                '<a href="javascript:addSearch(\'#$1\');">#$1</a>');
            
            $(elemSel + " .text").html(text);
            $(elemSel + " .created_at").text(elem.status.created_at.substring(0, 25));
            $(elemSel + " .score").text(elem.score);
            sources = "";
            if (elem.sources && elem.sources.length > 0) {
                $.each(elem.sources, function (i, s) {
                    sources += s + " ";
                });
            }
            if (sources.length > 0) {
                $(elemSel + " .source").text("via " + sources);
            }
            
            $(elemSel).click(function() {
                selectElement(elem.status.id);
            })
        }
        
        $(elemSel).removeClass('vote_up');
        $(elemSel).removeClass('vote_down');
        $(elemSel).removeClass('stat_up');
        $(elemSel).removeClass('stat_down');
        
        if (elem.vote) {
            //alert("has vote: " + elem.status.id + " : " + elem.vote.weight)
            if (elem.vote.weight > 0) {
                $(elemSel).addClass('vote_up');
            }    
            if (elem.vote.weight < 0) {
                $(elemSel).addClass('vote_down');
            }
        } else {
            if (elem.score < (gStatusStats.mean - gStatusStats.sd)) {
                $(elemSel).addClass('stat_down');
            } 
            if (elem.score > (gStatusStats.mean + gStatusStats.sd)) {
                $(elemSel).addClass('stat_up');
            }
        }
        
        if ($(elemSel).is(':hidden')) {
            if (gCurrentStatus > 0 && elem.status.id > gCurrentStatus) {
                $(elemSel).show();
            } else {
                $(elemSel).slideDown();
            }

        }
        
        $(elemSel + " .leftbox").click(function (e) {
            submitVote(elem, 1);
        });
        $(elemSel + " .rightbox").click(function (e) {
            submitVote(elem, -1);
        });
        
        if (freshPrince && (gCurrentStatus > 0) 
            && (elem.status.id > gCurrentStatus)) {
            $(document).scrollTop($(elemSel).outerHeight() + 
                $(document).scrollTop());
        }
    }
    
    statusComparator = function(a, b) {
        return (b.status.id - a.status.id);
    }
    
    mergeUpdate = function(data) {
        var firstLoad = false; 
        if (gStatusList.length == 0) {
            firstLoad = true;
        }
        
        $.each(data, function(idx, item) {
            if (indexOfId(item.status.id) == -1) {
                gStatusList.push(item);
            }
        });
        
        gStatusList.sort(statusComparator);
        if (gStatusList.length > 1000) {
            gStatusList = gStatusList.slice(0, 1000);
        }
        gStatusStats = standardScoreDeviation(gStatusList);

        displayAll();
        if (firstLoad) {
            selectElement(gStatusList[0].status.id);
        }
    }
    
    /* Load additional tweets from server. */
    loadNext = function() {
        since_id = null;
        if (gStatusList.length > 0) {
            since_id = gStatusList[0].status.id; 
        }
        loadFromServer(since_id);
    }
    
    loadFromServer = function (since_id) {
        $.getJSON('/twitterator/next', {'since_id': since_id}, function(data) {
            if (data[0].status) {
                mergeUpdate(data);
            } else {
                if (data.status) { 
                    // display server-side errors
                    warning(data.status);
                }
            }
            setTimeout(loadNext, 5000);
        })
    }
    
    // non-standard deviators will be shot!
    standardScoreDeviation = function (data) {
        var values = new Array(); 
        var r = new Object();
        if (data.length == 0) {
            return r;
        }
        r.mean = 0;
        $.each(data, function(idx, item) {
            values.push(item.score)
            r.mean += item.score;
        });
        r.mean /= values.length;
        sumdiff = 0;
        for (var i = 0; i < values.length; i++) {
            sumdiff += Math.pow(values[i]-r.mean, 2);
        }
        r.sd = Math.sqrt(sumdiff/values.length);
        return r;
    }
    
    
    /* Search management functionality */
    gSearches = new Array();
    
    fetchSearches = function () {
        $.getJSON('/search', function(json) {
            if (json.status && json.status == 'error') {
                warning("Adding search '" + term + "' failed; try again.");
            } else {
                gSearches = json; 
                $.each(gSearches, function(i, term) {
                    displaySearch(term);
                });
            }
        });
    }
    
    addSearch = function (term) {
        if ($.inArray(term, gSearches) != -1) {
            return;
        }
        if (term) {
            $.getJSON('/search/add', {'term': term }, function (json) {
                if (json.status && json.status == 'error') {
                    warning("Adding search '" + term + "' failed; try again.");
                } else {
                    gSearches.push(term);
                    displaySearch(json.term);
                    //loadFromServer(null);
                }
            });
        }
    }
    
    delSearch = function (term) {
        if ($.inArray(term, gSearches) == -1) {
            return;
        }
        $.getJSON('/search/del', {'term': term }, function (json) {
            if (json.status && json.status == 'error') {
                warning("Removing search '" + term + "' failed; try again.");
            } 
        });
    }
    
    displaySearch = function(term) {
        field = $("#protosearch").clone();
        field.attr("id", "s_tmp");
        field.insertAfter("#protosearch")
        $("#s_tmp span").text(term);
        elem = $("#s_tmp");
        $("#s_tmp span").click(function (e) {
            delSearch(term);
            $(e.target.parentNode).hide();
            
        })
        $("#s_tmp").show();
        $("#s_tmp").attr("id", null);
    }
    
    $(".user_tag span").click(function(e) {
        document.location.href = '/logout';
    });
    
    $("#search_add_form").submit(function (e) {
        addSearch($("#search_add").val());
        $("#search_add").val("");
        $("#search_add").blur();
        return false;
    });
    
    $(".search_icon").click(function (e) {
        $("#search_add_form").submit();
    })
    
    
    /* Voting AJAX */
    submitVote = function(elem, change) {
        var weight = elem.vote ? elem.vote.weight + change : change;
        weight = Math.max(Math.min(weight, 1), -1);
        if (elem.vote && elem.vote.weight == weight) {
            return;
        }
        if (!elem.vote) {
            if (weight == 1 && (elem.score < (gStatusStats.mean - gStatusStats.sd))) {
                weight = 0;
            } 
            if (weight == -1 && (elem.score > (gStatusStats.mean + gStatusStats.sd))) {
                weight = 0;
            }
        }
        var url = "/votes" + (elem.vote ? "/" + elem.vote.id : "") + ".json";
        $.post(url, {'weight': weight, 'tweet_id': elem.status.id}, function(reply) {
            if (reply.status) {
                // its a ... mistake
                warning(reply.message);
            } else {    
                idx = indexOfId(elem.status.id);
                gStatusList[idx].vote = reply;
                displayElem(gStatusList[idx]);
            }
        }, 'json');
    }
    
    
    
    // initial load.
    fetchSearches();
    loadNext();
    $(document).focus();
});