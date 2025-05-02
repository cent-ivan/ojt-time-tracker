#create error handling pages here like no priveleges, database error, connection/networking error

class SignUpErrorChecker:
    #error handling functions
    @staticmethod
    def signup_error_checker(err_type) -> str:
        match err_type:
            case 'email':
                return 'Email already taken. Use another email instead'
            case 'school':
                return 'School already registered'
            case 'user':
                return 'User already exists'
            case defaut:
                return f'(Some error: {err_type})'
    