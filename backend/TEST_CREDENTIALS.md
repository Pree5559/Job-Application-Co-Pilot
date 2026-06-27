# Test Credentials

## Existing User (Password Reset)

**Username:** `demo_user`  
**Password:** `test123`

✅ Password has been reset. You can now login with these credentials.

---

## Creating New Users

You can create new test users directly from the UI:

1. Go to http://localhost:8000
2. Use the **Sign Up** form (right side)
3. Enter any username and password (min 4 characters)
4. After signup, you'll be **automatically logged in** and see the main UI

---

## Testing Login After Logout

1. Click **Logout** button
2. Use the **Sign In** form (left side)
3. Enter the credentials you used during signup
4. Click **Login**
5. You should see the main UI immediately

---

## If You Forget a Password

Run this command in the backend directory:

```bash
.venv\Scripts\python reset_password.py <username> <new_password>
```

Example:
```bash
.venv\Scripts\python reset_password.py myuser newpass123
```

---

## What Was Fixed

### Issue 1: Login After Logout ✅
**Problem:** "Incorrect credentials" error after logout  
**Cause:** Password forgotten or not matching  
**Solution:** 
- Password for `demo_user` reset to `test123`
- Added better error messages
- Forms now clear after login/signup

### Issue 2: Signup Should Go to UI Directly ✅
**Problem:** After signup, required to sign in first  
**Cause:** Code was correct, but forms weren't clearing properly  
**Solution:**
- Already working - signup returns JWT token
- Added form field clearing
- Added success messages
- Better error handling

---

## Improvements Made

1. **Better Error Messages**
   - Login: "Please check your credentials"
   - Signup: "Username might already exist"
   - Validation: "Password must be at least 4 characters"

2. **Form Validation**
   - Username/password cannot be empty
   - Whitespace trimmed from username
   - Password minimum length: 4 characters

3. **Better UX**
   - Forms clear after successful login/signup
   - Success messages show welcome text
   - Logout clears all forms
   - Logout shows confirmation message

4. **Helpful Scripts**
   - `test_auth.py` - Check users and test passwords
   - `reset_password.py` - Reset any user's password

---

## Testing Steps

### Test 1: Login with Existing User
1. Go to http://localhost:8000
2. Sign In form (left side)
3. Username: `demo_user`
4. Password: `test123`
5. ✅ Should login successfully and show main UI

### Test 2: Create New User
1. Go to http://localhost:8000 (or refresh)
2. Sign Up form (right side)
3. Username: `testuser2` (or any unique name)
4. Password: `mypassword`
5. ✅ Should immediately show main UI after signup

### Test 3: Logout and Login Again
1. Click **Logout** button (top right)
2. ✅ Should show auth screen with success message
3. Sign In with the same credentials
4. ✅ Should login successfully

### Test 4: Enhanced File Upload
1. After login, go to "Create Application"
2. Hover over file upload area
3. ✅ Should turn blue
4. Click and select a PDF
5. ✅ Should show green card with filename
6. Click X button
7. ✅ Should clear selection

---

**Everything is fixed and ready to test!** 🎉
