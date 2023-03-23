const localStorageKey = '__pvtoken__'
async function client(endpoint, {body, ...customConfig} = {}, baseUrl, toJSON=true, stringify=true) {
  const storageToken = window.localStorage.getItem(localStorageKey)
  const token = storageToken? storageToken : window.sessionStorage.getItem(localStorageKey)
  const headers = {'content-type': 'application/json'}
  if (token) {
    headers.Authorization = `Token ${token}`
  }
  const config = {
    method: body ? 'POST' : 'GET',
    ...customConfig,
    headers: {
      ...headers,
      ...customConfig.headers,
    },
  }
  if (stringify && body) {
    config.body = JSON.stringify(body)
  } else if (body){
    config.body = body
  }
  /*HACKS
  */
  if (config.headers["content-type"]==='multipart/form-data'){
    delete config.headers["content-type"]
  }
 /*END HACKS*/
  console.log("CONFIG = ", config)
  return window
    .fetch(`${baseUrl}/${endpoint}`, config)
    .then(async response => {
      if (response.status === 401) {
        console.log("Logging out!")
        logout()
        window.location.assign(window.location)
        return
      }
      if (toJSON) {
        if (response.ok) {
          const data = await response.json()
          return data
        } else {
          return Promise.reject(response)
        }
      }
      else {
        if (response.ok){
          return response;
        } else {
          return Promise.reject(response);
        }
      }
    })
}
function logout() {
  window.localStorage.removeItem(localStorageKey)
  window.sessionStorage.removeItem(localStorageKey)
  window.localStorage.removeItem('username')
  window.sessionStorage.removeItem('username')
}
function isLoggedIn(){
    return window.localStorage.getItem(localStorageKey)?true:
    (window.sessionStorage.getItem(localStorageKey)? true:false);
}
// const prefix = "http://localhost:8000"
const prefix = ""
export {client, localStorageKey, logout, isLoggedIn, prefix}