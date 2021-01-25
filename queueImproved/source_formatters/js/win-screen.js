let time = Math.floor(Date.now() / 1000);
const importConfig = () => import('../../../config.js');
let bully = {};
let playing = false;
function loop(client_id, client_secret, filepath) {
    const importWinScreen = () => import(filepath + '?t=' + time);
    importWinScreen().then(function (resp) {
        const winning_player = resp.default.winning_player;
        const next_player = resp.default.next_player;
        const winning_side = resp.default.winning_side;
        let now = Math.floor(Date.now() / 1000);
        if(now <= resp.default.timestamp + 2) {
            if(winning_player) {
                if(winning_player.username !== " ") {
                    $(".side").removeClass('winner');
                    $(".side:nth-child(" + winning_side + ")").addClass('winner');
                let animateBully = false;
                if (resp.default.bully) {
                    if (bully.username) {
                        console.log(resp.default.bully.username);
                        if (bully.username !== resp.default.bully.username) {
                            animateBully = true;
                            bully = resp.default.bully;
                        }
                    }
                    else {
                        console.log("here");
                        animateBully = true;
                        bully = resp.default.bully;
                    }
                }
                let xhr = new XMLHttpRequest();
                xhr.open("POST", "https://id.twitch.tv/oauth2/token", true);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
                xhr.setRequestHeader('Accept', 'application/json');
                xhr.send('client_id='+ client_id +'&client_secret='+ client_secret +'&grant_type=client_credentials');
                xhr.onreadystatechange = function () {
                    if (xhr.readyState === 4) {
                        const response = JSON.parse(xhr.response);
                        const xhr1 = new XMLHttpRequest();
                        xhr1.open("GET", "https://api.twitch.tv/helix/users?login=" + winning_player.username, true);
                        xhr1.setRequestHeader('Client-ID', client_id);
                        xhr1.setRequestHeader('Authorization', 'Bearer ' + response.access_token);
                        xhr1.onreadystatechange = function() {
                            if (xhr1.readyState === 4) {
                                const response1 = JSON.parse(xhr1.response);
                                // console.log(response1);
                                $('.winner .player-pic').attr("src", response1.data[0].profile_image_url);
                                $('.winner .player-name').html(winning_player.username);
                                $('.winner .old-wins').html(parseInt(winning_player.set_streak) - 1);
                                $('.winner .new-wins').html(parseInt(winning_player.set_streak));
                                if(next_player.username) {
                                    xhr = new XMLHttpRequest();
                                    xhr.open("POST", "https://id.twitch.tv/oauth2/token", true);
                                    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
                                    xhr.setRequestHeader('Accept', 'application/json');
                                    xhr.send('client_id='+ client_id +'&client_secret='+ client_secret +'&grant_type=client_credentials');
                                    xhr.onreadystatechange = function () {
                                        if (xhr.readyState === 4) {
                                            const response1 = JSON.parse(xhr.response);
                                            const xhr2 = new XMLHttpRequest();
                                            xhr2.open("GET", "https://api.twitch.tv/helix/users?login=" + next_player.username, true);
                                            xhr2.setRequestHeader('Client-ID', client_id);
                                            xhr2.setRequestHeader('Authorization', 'Bearer ' + response1.access_token);
                                            xhr2.onreadystatechange = function() {
                                                if (xhr2.readyState === 4) {
                                                    const response2 = JSON.parse(xhr2.response);
                                                    console.log(response2);
                                                    $('.side:not(.winner) .player-pic').attr("src", response2.data[0].profile_image_url);
                                                    $('.side:not(.winner)  .player-name').html(next_player.username);
                                                    if(animateBully) {
                                                        console.log(winning_player);
                                                        console.log(bully);
                                                        if(winning_player.username === bully.username) {

                                                            $('#new-bully .player-pic')[0].attr("src", response1.data[0].profile_image_url);
                                                            $('#new-bully .player-name')[0].html(bully.username);
                                                            animateWinScreen(winning_side,true, animateBully);
                                                        }
                                                    } else {
                                                        animateWinScreen(winning_side,true, animateBully);
                                                    }
                                                }
                                            }
                                            xhr2.onerror = function(error){
                                              // console.log(error.target.status);
                                            };
                                            xhr2.send();
                                        }
                                    };
                                }
                                else {
                                    if(winning_player.username === bully.username) {
                                        $('#new-bully .player-pic').get(0).setAttribute("src", response1.data[0].profile_image_url);
                                        $('#new-bully .player-name').get(0).innerHTML = bully.username;
                                        animateWinScreen(winning_side,false, animateBully);
                                    } else
                                        animateWinScreen(winning_side,false, animateBully)
                                }
                            }
                        }
                        xhr1.onerror = function(error){
                          // console.log(error.target.status);
                        };
                        xhr1.send();
                    }
                };
            }
            }
        }
        time = Math.floor(Date.now() / 1000);
        setTimeout(function() { loop(client_id, client_secret, filepath) }, 1000)
    });
}
function startLoop(filepath) {
    importConfig().then(function(resp) {
        loop(resp.default.client_id, resp.default.client_secret, filepath);
    })
}
function animateWinScreen(winningSide, isNextPlayer, animateBully) {
    if(!playing) {
        playing = true;
        $(".side").removeClass('slide-out');
        $(".player-info").removeClass('flash');
        $(".wins").removeClass('scroll-up');

        $(".winner").addClass('slide-in');
        setTimeout(function() {
            $(".winner .fas-1").animate({"top": "-21px", "opacity": "0.2"}, 500)
            $(".winner .fas-2").animate({"top": "0px", "opacity": "1"}, 700)
        }, 750)
        setTimeout(function() {
            // $(".winner .old-wins").animate({"top": "-30px", "opacity": "0.2"}, 500)
            // $(".winner .new-wins").animate({"top": "0px", "opacity": "1"}, 700)
            $(".wins").addClass('scroll-up');
        }, 1200)
        setTimeout(function() {
             $(".side.winner .player-info").addClass('flash');
        }, 2000);
        if(isNextPlayer) {
            setTimeout(function() {
                $(".side:not(.winner)").addClass('slide-in');
        }, 2500);
        }
        setTimeout(function() {
            $(".side").removeClass('slide-in');
            if(isNextPlayer)
                $(".side").addClass('slide-out');
            else
                $(".winner").addClass('slide-out');
            if(!animateBully)
                playing = false;
        }, 5000);
        if(animateBully) {
            setTimeout(function () {
                $('#static').addClass('active');
            }, 6000)
            setTimeout(function () {
                $('#static').removeClass('active');
                $('#new-bully').addClass('active');
                $('#new-bully video')[0].play();
            }, 7000)
            setTimeout(function () {
                $('#new-bully').removeClass('active');
                $('#static').addClass('active');
            }, 9700)
            setTimeout(function () {
                $('#static').removeClass('active');
                playing = false;
            }, 10700)
        }
        // setTimeout(function() {
        //     $(".winner .old-wins").css({"top": "0px", "opacity": "1"})
        //     $(".winner .new-wins").css({"top": "-30px", "opacity": "0.2"})
        // }, 6000)
    }
}
startLoop("../../source_content/win-screen.js")