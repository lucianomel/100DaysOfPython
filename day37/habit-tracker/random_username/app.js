const bcrypt = require("bcrypt")
const saltRounds = 10


bcrypt
  .genSalt(saltRounds)
  .then(salt => {
    console.log('Salt: ', salt)
  })
  .catch(err => console.error(err.message))