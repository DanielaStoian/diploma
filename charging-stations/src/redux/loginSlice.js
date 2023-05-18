import { createSlice } from '@reduxjs/toolkit'

export const loginSlice = createSlice({
  name: 'login',
  initialState: {
    value: false,
    user_id:0,
  },
  reducers: {
    logIn: (state) => {
      // Redux Toolkit allows us to write "mutating" logic in reducers. It
      // doesn't actually mutate the state because it uses the Immer library,
      // which detects changes to a "draft state" and produces a brand new
      // immutable state based off those changes
      state.value = true
    },
    logOut: (state) => {
      state.value = false
    },
    setUserId: (state, prop) => {
        console.log(prop)
        state.user_id = prop.payload
      }
  },
})

// Action creators are generated for each case reducer function
export const { logIn, logOut, setUserId } = loginSlice.actions

export default loginSlice.reducer