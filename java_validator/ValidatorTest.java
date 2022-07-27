import static org.assertj.core.api.Assertions.assertThat;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.junit.jupiter.api.Test;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.time.LocalDate;
import javax.validation.Constraint;
import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;
import javax.validation.Payload;
import javax.validation.Valid;
import javax.validation.Validation;
import javax.validation.Validator;
import javax.validation.ValidatorFactory;

public class ValidatorTest {

    @Test
    void should_validate_user_properties() {
        final UserBirthdayShouldMatchIdentityValidator validator = new UserBirthdayShouldMatchIdentityValidator();

        assertThat(validator.isValid(new User("some identity", LocalDate.now()), null)).isFalse();
    }

    @Test
    void should_validate_user_properties_use_jsr() {
        ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
        Validator validator = factory.getValidator();
        var violations = validator.validate(new User("some identity", LocalDate.now()));
        assertThat(violations.size()).isEqualTo(1);
        assertThat(violations.stream().findFirst().get().getMessage()).isEqualTo("User birthday should match identity");
    }

    public static class UserBirthdayShouldMatchIdentityValidator implements
            ConstraintValidator<UserBirthdayShouldMatchIdentityValidator.UserBirthdayShouldMatchIdentity,
                    UserBirthdayShouldMatchIdentityValidator.BirthdayAndIdentity> {

        public UserBirthdayShouldMatchIdentityValidator() { }

        @Override
        public void initialize(UserBirthdayShouldMatchIdentity constraintAnnotation) {
        }

        @Override
        public boolean isValid(BirthdayAndIdentity value, ConstraintValidatorContext context) {
            System.out.println("validating...");
            return false;
        }


        @Target(ElementType.TYPE)
        @Retention(RetentionPolicy.RUNTIME)
        @Constraint(validatedBy = UserBirthdayShouldMatchIdentityValidator.class)
        public @interface UserBirthdayShouldMatchIdentity {

            String message() default "User birthday should match identity";

            Class<?>[] groups() default { };

            Class<? extends Payload>[] payload() default { };
        }

        public interface BirthdayAndIdentity {

            String getIdentity();

            LocalDate getBirthday();
        }

    }

    @Valid
    @Data
    @AllArgsConstructor
    @UserBirthdayShouldMatchIdentityValidator.UserBirthdayShouldMatchIdentity
    public static class User implements UserBirthdayShouldMatchIdentityValidator.BirthdayAndIdentity {

        private String identity;
        private LocalDate birthday;
    }

}
