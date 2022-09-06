ME_QUERY = \
'''
query me {
    me {
        username
        isSuperuser
    }
}
'''

CREATE_USER_MUTATION = \
'''
mutation createUser($email: String!, $username: String!, $password: String!, $firstName: String, $lastName: String, $isStaff: Boolean) {
  createUser(email: $email, username: $username, password: $password, firstName: $firstName, lastName: $lastName, isStaff: $isStaff) {
    user {
      id
      username
      firstName
      lastLogin
      isSuperuser
      isStaff
      isActive
      dateJoined


    }
  }
}
'''