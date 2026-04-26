package com.esgnexus.service;

import com.esgnexus.domain.Usuario;
import com.esgnexus.dto.AuthDtos;
import com.esgnexus.repository.UsuarioRepository;
import com.esgnexus.security.JwtService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthService {
    private final AuthenticationManager authenticationManager;
    private final UsuarioRepository usuarioRepository;
    private final JwtService jwtService;

    public AuthDtos.LoginResponse login(AuthDtos.LoginRequest request) {
        // authenticationManager.authenticate(new UsernamePasswordAuthenticationToken(request.email(), request.senha()));
        Usuario usuario = usuarioRepository.findByEmail(request.email()).orElseThrow();
        String token = jwtService.generateToken(new org.springframework.security.core.userdetails.User(
                usuario.getEmail(), usuario.getSenhaHash(), java.util.List.of()));
        return new AuthDtos.LoginResponse(token, usuario.getNome(), usuario.getEmail(), usuario.getPerfil());
    }
}
