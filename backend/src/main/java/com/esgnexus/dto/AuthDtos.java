package com.esgnexus.dto;

import com.esgnexus.domain.Role;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

public class AuthDtos {
    public record LoginRequest(@Email @NotBlank String email, @NotBlank String senha) {}
    public record LoginResponse(String token, String nome, String email, Role perfil) {}
}
