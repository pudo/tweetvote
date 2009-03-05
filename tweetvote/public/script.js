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
        if (-1 == indexOfId(tweet_id)) {
            return false
        }
        oldSel = '#tweet_' + gCurrentStatus;
        gCurrentStatus = tweet_id;
        $(oldSel).removeClass("current");
        newSel = '#tweet_' + tweet_id;
        $(newSel).addClass("current");
        //followSelection();
        return true;
    }
    
    followSelection = function() {
        cur = $('#tweet_' + gCurrentStatus);
        pagePart = ($(window).height()/4);
        viewportTop = $(document).scrollTop();
        scrolledPos = cur.position().top - viewportTop;
        //alert("Scrolled: " + scrolledPos);
        if (scrolledPos > pagePart * 3) {
            $(document).scrollTop(viewportTop 
                + cur.outerHeight());
        } 
        if (scrolledPos < pagePart) {
            $(document).scrollTop(viewportTop    
                - cur.outerHeight());
        }
    }
    
    $(window).scroll(function(event) {
        viewportTop = $(document).scrollTop();
        viewportBottom = viewportTop + $(window).height();
        cur = $('#tweet_' + gCurrentStatus);
        currentTop = cur.position().top;
        currentBottom = currentTop + cur.outerHeight();
        idx = indexOfId(gCurrentStatus);
        
        if (currentTop < viewportTop) {
            idx++;
            if (idx < gStatusList.length) {
                selectElement(gStatusList[idx].status.id);
            }
        }
        if (currentBottom > viewportBottom) {
            idx--;
            if (idx >= 0) {
                selectElement(gStatusList[idx].status.id);
            }
        }
    });
    
    /* Keyboard mappings */
    $(document).keydown(function(e) {
        switch(e.which) {
            case 40: // cur down
                newIndex = indexOfId(gCurrentStatus) + 1; 
                if (gStatusList.length > newIndex) {
                    selectElement(gStatusList[newIndex].status.id); 
                    followSelection();
                }
                break;
            case 38: // cur up.
                newIndex = indexOfId(gCurrentStatus) - 1; 
                if (newIndex >= 0) {
                    selectElement(gStatusList[newIndex].status.id); 
                    followSelection();
                }
                break;
            case 37: // cur left
                idx = indexOfId(gCurrentStatus);
                submitVote(gStatusList[idx], -1);
                break;
            case 39: // cur right
                idx = indexOfId(gCurrentStatus);
                submitVote(gStatusList[idx], 1);
                break;
            case 83:
                term = prompt("Enter your search term:");
                addSearch(term);
                loadNext();
        }
        //return false;
        //alert(e.which);
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
        if (!$(elemSel).length) { // a new one
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
                '<a target="_new" href="http://search.twitter.com/search?q=%23$1">#$1</a>');
            
            $(elemSel + " .text").html(text);
            $(elemSel + " .created_at").text(elem.status.created_at);
            $(elemSel + " .score").text(elem.score);
            
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
            $(elemSel).slideDown();
        }
    }
    
    statusComparator = function(a, b) {
        return (b.status.id - a.status.id);
    }
    
    mergeUpdate = function(data) {
        $.each(gStatusList, function(idx, item) {
            if ($.inArray(item, data) == -1) {
                data.push(item);
            }
        });
        
        gStatusList = data;
        gStatusList.sort(statusComparator);
        gStatusStats = standardScoreDeviation(gStatusList);
        
        displayAll();
        selectElement(gStatusList[0].status.id);
    }
    
    /* Load additional tweets from server. */
    loadNext = function() {
        since_id = null;
        if (gStatusList.length > 0) {
            since_id = gStatusList[0].status.id; 
        } 
        $.getJSON('/twitterator/next', {'since_id': since_id}, function(data) {
            if (data[0].status) {
                mergeUpdate(data);
            } else {
                if (data.status) { 
                    // display server-side errors
                    warning(data.status);
                }
            }
            setTimeout(loadNext, 15000);
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
    fetchSearches = function (f) {
        $.getJSON('/search', f);
    }
    
    addSearch = function (term) {
        $.getJSON('/search/add', {'term': term }, function (json) {
            if (json.status == 'error' || $.inArray(term, json) == -1) {
                warning("Adding search '" + term + "' failed; try again.");
            }
        });
    }
    
    delSearch = function (term) {
        $.getJSON('/search/del', {'term': term }, function (json) {
            if (json.status == 'error' || $.inArray(term, json) != -1) {
                warning("Removing search '" + term + "' failed; try again.");
            }
        });
    }
    
    delSearchCurry = function(term) {
        return function () { 
            delSearch(term); 
        };
    }
    
    /* Voting AJAX */
    submitVote = function(elem, change) {
        var weight = elem.vote ? elem.vote.weight + change : change;
        weight = Math.max(Math.min(weight, 1), -1);
        if (elem.vote && elem.vote.weight == weight) {
            return;
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
    loadNext();
    
});