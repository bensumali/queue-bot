let time = Math.floor(Date.now() / 1000);
const importConfig = () => import('../../../config.js');
let currentUsername = "";
function loop(client_id, client_secret, filepath) {
    const importPlayer1Name = () => import(filepath + '?t=' + time);
    importPlayer1Name().then(function (resp) {
        const username = resp.default.username;
        if(currentUsername != username) {
            currentUsername = username;

            const xhr = new XMLHttpRequest();
            xhr.open("POST", "https://id.twitch.tv/oauth2/token", true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
            xhr.setRequestHeader('Accept', 'application/json');
            xhr.send('client_id='+ client_id +'&client_secret='+ client_secret +'&grant_type=client_credentials');
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4) {
                    console.log(xhr.response);
                    const response = JSON.parse(xhr.response);
                    const xhr1 = new XMLHttpRequest();
                    xhr1.open("GET", "https://api.twitch.tv/helix/users?login=" + username, true);
                    xhr1.setRequestHeader('Client-ID', 'bcnkezzrtah276cw73d86sytx2b064');
                    xhr1.setRequestHeader('Authorization', 'Bearer ' + response.access_token);
                    xhr1.onreadystatechange = function() {
                    if (xhr1.readyState === 4) {
                          const response1 = JSON.parse(xhr1.response);
                          console.log(response1);
                          document.getElementById("player-pic").src = " ";
                          setTimeout(function() {
                              document.getElementById("player-pic").src = response1.data[0].profile_image_url;
                          }, 1000);
                        }
                      }
                    xhr1.onerror = function(error){
                      console.log(error.target.status);
                    };
                    xhr1.send();
                }
            };


        }
        time = Math.floor(Date.now() / 1000);
        setTimeout(function() { loop(client_id, client_secret, filepath) }, 1000)
    });
}
function getUserData(filepath) {
    importConfig().then(function(resp) {
        loop(resp.default.client_id, resp.default.client_secret, filepath);
    })
}











